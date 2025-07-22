#!/usr/bin/env python3
"""
📟 Raspberry Pager
Send and receive text messages via RF (e.g., RFM69) using Raspberry Pi GPIO.
"""

import time
import threading
import argparse
import queue
from datetime import datetime

try:
    import RPi.GPIO as GPIO
    from pydantic import BaseModel
    # Dummy placeholder import for RF library; replace with your actual RF module
    from rf_module import RF69  # pretend RF transceiver library
except ImportError:
    print("Missing dependencies: RPi.GPIO, pydantic, rf_module")
    exit(1)

# DEFAULT SETTINGS
RF_FREQ = 915.0  # MHz
NODE_ID = 1
TARGET_ID = 2
MESSAGE_QUEUE = queue.Queue()
STOP_EVENT = threading.Event()


# 📨 Message structure
class Message(BaseModel):
    timestamp: str
    sender_id: int
    receiver_id: int
    text: str

    def serialize(self) -> bytes:
        return f"{self.timestamp}|{self.sender_id}|{self.receiver_id}|{self.text}".encode()

    @classmethod
    def deserialize(cls, data: bytes):
        parts = data.decode().split("|", 3)
        return cls(
            timestamp=parts[0],
            sender_id=int(parts[1]),
            receiver_id=int(parts[2]),
            text=parts[3]
        )


def setup_rf(freq_mhz: float) -> RF69:
    rf = RF69(freq_mhz)
    rf.init()
    rf.set_node_id(NODE_ID)
    return rf


def sender_loop(rf: RF69):
    while not STOP_EVENT.is_set():
        try:
            msg = MESSAGE_QUEUE.get(timeout=1)
        except queue.Empty:
            continue
        rf.send(msg.receiver_id, msg.serialize())
        print(f"🟢 Sent to {msg.receiver_id} @ {msg.timestamp}: "{msg.text}"")


def receiver_loop(rf: RF69):
    while not STOP_EVENT.is_set():
        packet = rf.receive(timeout=0.5)
        if packet:
            msg = Message.deserialize(packet)
            if msg.receiver_id == NODE_ID:
                print(f"📥 Received from {msg.sender_id} @ {msg.timestamp}: "{msg.text}"")


def user_input_loop(receiver_id: int):
    while not STOP_EVENT.is_set():
        try:
            text = input("Enter message > ")
            if text.strip().lower() in ["exit", "quit"]:
                STOP_EVENT.set()
                break
            msg = Message(
                timestamp=datetime.now().isoformat(),
                sender_id=NODE_ID,
                receiver_id=receiver_id,
                text=text
            )
            MESSAGE_QUEUE.put(msg)
        except (EOFError, KeyboardInterrupt):
            STOP_EVENT.set()
            break


def main():
    parser = argparse.ArgumentParser(description="📟 Raspberry Pager")
    parser.add_argument("--freq", type=float, default=RF_FREQ, help="RF frequency in MHz")
    parser.add_argument("--dest", type=int, default=TARGET_ID, help="Destination node ID")
    args = parser.parse_args()

    rf = setup_rf(args.freq)
    print(f"✅ RF initialized at {args.freq} MHz, node ID {NODE_ID}")

    t_send = threading.Thread(target=sender_loop, args=(rf,), daemon=True)
    t_recv = threading.Thread(target=receiver_loop, args=(rf,), daemon=True)
    t_input = threading.Thread(target=user_input_loop, args=(args.dest,), daemon=True)

    t_send.start()
    t_recv.start()
    t_input.start()

    try:
        while not STOP_EVENT.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        STOP_EVENT.set()

    print("🛑 Shutting down...")

if __name__ == "__main__":
    main()

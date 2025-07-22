# 📟 Raspberry Pager (Raspberry Pi)

Send and receive short text messages over RF between Raspberry Pi units—no internet required! Ideal for off-grid communication, emergency alerts, or DIY messaging networks.


## 🚀 Features

- 📶 Uses RF transceiver (e.g., RFM69) for peer-to-peer messaging  
- 🧩 Modular design with **Message** data model (timestamp, sender, receiver, text)  
- 🔁 Asynchronous send and receive loops  
- 🧵 Thread-safe queue and clean shutdown signaling  
- 📝 CLI interface—type messages, hit Enter to send  
- ✂️ Minimal dependencies: `RPi.GPIO`, `pydantic`, RF library


## 🧰 Requirements

- Raspberry Pi 5 (any Pi model works with minor adjustments)  
- RF module (e.g., RFM69 or nRF24L01) connected via GPIO/SPI  
- Python 3.7+  
- Install dependencies:
  ```bash
  pip install pydantic RPi.GPIO
  # and your RF library, e.g., git+https://github.com/your/rf_module
  ```


## 📦 File Structure

```
📟 Raspberry-Pager-RPi/
├── pager.py         # Main code (~200 lines)
└── README.md        # This documentation
```


## ⚙️ Setup & Wiring

1. Wire your RF module to SPI and GPIO (CS, IRQ, etc.).  
2. Run `pager.py` with appropriate frequency and recipient ID:
   ```bash
   python3 pager.py --freq 915 --dest 2
   ```
3. Launch a second Pi with `. --dest 1` to communicate back and forth.


## 🧠 How It Works

- **RF Init:** `setup_rf()` initializes the RF hardware.  
- **Message Model:** Clean JSON-like structure with serialization.  
- **Sending Thread:** Reads messages from a queue and transmits via RF.  
- **Receiving Thread:** Listens for incoming packets and prints them.  
- **User Thread:** Terminal input pushes outgoing messages.  
- 🛡️ **Graceful shutdown** via input command or Ctrl+C.


## 💡 Tips & Tweaks

- Use `pydantic` to validate and extend message structure (e.g., add delivery status).  
- Use logging vs. `print()` for robust debugging.  
- Add command shortcuts (e.g., `/who` to ping peers).  
- Include retries or acknowledgments for reliability.


## 📶 Expansions

- 🏡 Mesh network across multiple Pis  
- 🔊 Audio alerts for received messages  
- 📦 Companion web UI  
- 🖼️ SMS-like thread logging

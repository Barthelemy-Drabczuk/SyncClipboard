# SyncClipboard - Synchronized Clipboard Across All Devices

![Status](https://img.shields.io/badge/status-MVP-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

A real-time clipboard synchronization system that allows you to share clipboard content across multiple devices. Copy on one device, paste on another!

## Features

- **Real-time Synchronization**: Clipboard updates propagate instantly to all your devices
- **Text & Image Support**: Copy and sync both text and images seamlessly
- **Observer Pattern**: Clean architecture with event-driven clipboard monitoring
- **WebSocket Support**: Live updates without polling
- **Web Interface**: View and manage your clipboard history in a browser with image previews
- **Secure Storage**: All clipboard entries stored in MongoDB
- **Multi-Device**: Connect unlimited devices with the same account
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Quick Start

See [SETUP.md](SETUP.md) for detailed installation and setup instructions.

### Basic Usage

1. **Start the server**:
   ```bash
   cd src
   python webapp.py
   ```

2. **Register at** `http://localhost:5000`

3. **Start the client**:
   ```bash
   python main_client.py --user-id YOUR_USER_ID
   ```

4. **Copy text** (Ctrl+C) and watch it sync across devices!

## Architecture

The system consists of four main components:

### 1. Desktop Client ([client.py](src/client.py))
- Monitors keyboard events (Ctrl+C/V) using `pynput`
- Implements observer pattern to notify server of clipboard changes
- Manages local clipboard buffer
- Receives real-time updates via WebSocket

### 2. Web Server ([webapp.py](src/webapp.py))
- Flask-based REST API for clipboard operations
- WebSocket server using Flask-SocketIO
- User authentication and registration
- Real-time push notifications to connected clients

### 3. Database Layer ([db_management.py](src/db_management.py))
- MongoDB for data persistence
- CRUD operations for users and clipboard transactions
- Stores clipboard history with timestamps

### 4. Web Interface ([templates/index.html](src/templates/index.html))
- Modern, responsive UI for viewing clipboard history
- Real-time updates via WebSocket
- User authentication (login/register)
- Displays clipboard entries with timestamps

## Technology Stack

- **Backend**: Python 3.8+, Flask, Flask-SocketIO
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript, Socket.IO
- **Clipboard**: pyperclip, pynput
- **Communication**: HTTP REST API, WebSocket
- **Package Management**: pyproject.toml (PEP 517/518 compliant)

## Project Structure

```
SyncClipboard/
├── src/
│   ├── client.py              # Desktop client (keyboard monitoring)
│   ├── webapp.py              # Web server (Flask + SocketIO)
│   ├── main_client.py         # Client launcher script
│   ├── db_management.py       # Database CRUD operations
│   ├── clipboard_observer.py  # Observer pattern implementation
│   ├── websocket_client.py    # WebSocket client for receiving updates
│   ├── clip_user.py           # User model
│   ├── clip_object.py         # Clipboard object model
│   ├── templates/
│   │   └── index.html         # Web interface
│   └── tests/                 # Unit tests
├── pyproject.toml             # Package configuration & dependencies
├── docker-compose.yml         # Docker setup
├── Dockerfile                 # Webapp container
├── README.md                  # This file
├── SETUP.md                   # Detailed setup guide
├── DOCKER.md                  # Docker deployment guide
└── CONTRIBUTING.md            # Contribution guidelines
```

## How It Works

1. **Copy Detection**: Desktop client monitors Ctrl+C keypresses
2. **Notify Server**: When clipboard changes, client sends content to server via HTTP POST
3. **Store in Database**: Server stores the clipboard entry in MongoDB
4. **Broadcast Update**: Server broadcasts the update to all connected clients via WebSocket
5. **Sync Clipboards**: All devices receive the update and can access the content
6. **Web History**: View all clipboard history in the web interface

## Development Timeline

### Update 13/02/23
- Switched to [Pyperclip](https://pypi.org/project/pyperclip/) for clipboard operations
- Using [Pynput](https://pypi.org/project/pynput/) for keyboard event capture

### Update 12/02/23
- Switched from SQL to NoSQL (MongoDB) for better scalability
- MongoDB chosen for Python compatibility and document storage

### MVP Completed (Current)
- ✅ Full CRUD operations for database
- ✅ Observer pattern implementation
- ✅ Real-time WebSocket synchronization
- ✅ Web interface for clipboard history
- ✅ User authentication system
- ✅ Multi-client support

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login existing user

### Clipboard Operations
- `POST /api/clipboard` - Add new clipboard entry
- `GET /api/clipboard/<user_id>` - Get clipboard history

### WebSocket Events
- `connect` - Client connects to server
- `join` - Join user-specific room for updates
- `clipboard_update` - Receive clipboard updates

## Security Notes

⚠️ **This is an MVP**. For production use, consider:
- Implementing proper authentication tokens (JWT)
- Encrypting clipboard content
- Using HTTPS/WSS
- Rate limiting
- Input validation and sanitization
- Secure password hashing (currently using Python's `hash()`)

## Future Enhancements

- [ ] Image and file clipboard support
- [ ] End-to-end encryption
- [ ] Desktop GUI application
- [ ] Mobile apps (iOS/Android)
- [ ] Clipboard search and filtering
- [ ] Item deletion and management
- [ ] Clipboard categories/tags
- [ ] Offline support with sync queue

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for learning or commercial purposes.

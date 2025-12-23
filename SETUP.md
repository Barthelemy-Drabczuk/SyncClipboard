# SyncClipboard - Setup Guide

This guide will help you set up and run the SyncClipboard MVP.

## Setup Options

Choose one of the following setup methods:

1. **[Docker Setup](#docker-setup)** (Recommended) - Easy, containerized deployment
2. **[Manual Setup](#manual-setup)** - Traditional installation with local MongoDB

---

## Docker Setup

See [DOCKER.md](DOCKER.md) for detailed Docker deployment instructions.

### Quick Start with Docker

```bash
# Start services
docker-compose up -d

# Access the webapp
open http://localhost:5000

# View logs
docker-compose logs -f
```

---

## Manual Setup

### Prerequisites

1. **Python 3.8+** installed
2. **MongoDB** installed and running
3. **pip** for package management

## Installation

### 1. Install MongoDB

**Ubuntu/Debian:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**macOS:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Check MongoDB is running:**
```bash
# Should connect to MongoDB shell
mongo
```

### 2. Install Python Dependencies

Install the package using pyproject.toml:

**Standard installation:**
```bash
pip install -e .
```

**With development tools (pytest, black, flake8, mypy):**
```bash
pip install -e ".[dev]"
```

## Running the Application

### Step 1: Start MongoDB

Make sure MongoDB is running on your system:
```bash
sudo systemctl status mongodb  # Linux
brew services list | grep mongodb  # macOS
```

### Step 2: Start the Web Server

In one terminal, navigate to the `src` directory and run:

```bash
cd src
python webapp.py
```

The server will start on `http://localhost:5000`

You should see:
```
 * Running on http://0.0.0.0:5000
```

### Step 3: Register a User (Web Interface)

1. Open your browser and go to `http://localhost:5000`
2. Click "Register Instead"
3. Create an account with:
   - Username
   - Email
   - Password
4. After registration, you'll see your clipboard history page
5. **Note your User ID** - you'll see it in the browser console or you can find it by checking the MongoDB database

### Step 4: Get Your User ID

You have several options:

**Option A - Browser Console:**
- Open browser DevTools (F12)
- Look for the login/register response which includes `user_id`

**Option B - MongoDB Shell:**
```bash
mongo
use prod_env
db.users.find()
```

Look for your username and note the `id` field.

### Step 5: Start the Desktop Client

In another terminal:

```bash
cd src
python main_client.py --user-id YOUR_USER_ID --server http://localhost:5000
```

Replace `YOUR_USER_ID` with the ID you obtained in Step 4.

## Testing the System

### Test 1: Copy Detection
1. With the client running, copy some text (Ctrl+C)
2. Check the terminal - you should see clipboard update messages
3. Refresh the web interface - your copied text should appear in the history

### Test 2: Real-time Sync
1. Keep the web interface open
2. Copy text with the client running
3. The web interface should update in real-time (without refresh) showing the new clipboard entry

### Test 3: Multi-Device Sync
1. Start multiple clients with the same user ID on different terminals/machines
2. Copy text on one client
3. All clients should receive the update via WebSocket
4. The web interface should show all updates in real-time

## Architecture Overview

```
┌─────────────────┐
│  Desktop Client │  (Monitors Ctrl+C/V)
│   (main_client) │
└────────┬────────┘
         │
         │ HTTP POST (clipboard content)
         │ WebSocket (receive updates)
         ↓
┌─────────────────┐
│   Web Server    │  (Flask + SocketIO)
│   (webapp.py)   │
└────────┬────────┘
         │
         │ Store/Retrieve
         ↓
┌─────────────────┐
│    MongoDB      │  (Database)
│  prod_env.users │
│  .transactions  │
└─────────────────┘
         ↑
         │ View History
         │
┌─────────────────┐
│  Web Interface  │  (Browser)
│ (index.html)    │
└─────────────────┘
```

## Key Features Implemented

1. **Observer Pattern**: Client notifies server when clipboard changes
2. **Real-time Updates**: WebSocket pushes updates to all connected clients
3. **Web Interface**: View clipboard history in browser
4. **User Management**: Registration and login system
5. **Database Persistence**: All clipboard entries stored in MongoDB

## Troubleshooting

### MongoDB Connection Error
```
Error: pymongo.errors.ServerSelectionTimeoutError
```
**Solution**: Make sure MongoDB is running:
```bash
sudo systemctl start mongodb
```

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Change the port in `webapp.py`:
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5001)
```

### WebSocket Connection Failed
**Solution**: Make sure the server URL in the client matches where the server is running:
```bash
python main_client.py --user-id YOUR_ID --server http://localhost:5000
```

## Next Steps

- Add authentication tokens instead of plain user IDs
- Implement clipboard content encryption
- Add image/file clipboard support
- Create desktop GUI for easier user management
- Add clipboard search functionality
- Implement clipboard item deletion

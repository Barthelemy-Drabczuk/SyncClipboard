import socketio
import pyperclip
import threading


class WebSocketClipboardClient:
    """Client that connects to the server via WebSocket for real-time updates"""

    def __init__(self, server_url: str, user_id: int):
        """Initialize the WebSocket client

        Args:
            server_url (str): The URL of the server
            user_id (int): The user's ID
        """
        self.server_url = server_url
        self.user_id = user_id
        self.sio = socketio.Client()

        # Register event handlers
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('clipboard_update', self.on_clipboard_update)

    def on_connect(self):
        """Handle connection to server"""
        print(f'Connected to server at {self.server_url}')
        self.sio.emit('join', {'user_id': self.user_id})

    def on_disconnect(self):
        """Handle disconnection from server"""
        print('Disconnected from server')

    def on_clipboard_update(self, data):
        """Handle clipboard update from server

        Args:
            data (dict): Update data containing content and timestamp
        """
        content = data.get('content')
        if content:
            print(f'Received clipboard update: {content[:50]}...')
            # Update local clipboard
            pyperclip.copy(content)

    def connect(self):
        """Connect to the server"""
        try:
            self.sio.connect(self.server_url)
        except Exception as e:
            print(f'Error connecting to server: {e}')

    def disconnect(self):
        """Disconnect from the server"""
        if self.sio.connected:
            self.sio.disconnect()

    def wait(self):
        """Wait for the connection to close"""
        self.sio.wait()

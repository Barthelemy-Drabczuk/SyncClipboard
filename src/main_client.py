#!/usr/bin/env python3
"""
Main client application that combines clipboard monitoring with server sync
"""
import sys
import argparse
from client import Client
from clipboard_observer import ServerClipboardObserver
from websocket_client import WebSocketClipboardClient
import threading


def main():
    parser = argparse.ArgumentParser(
        description='SyncClipboard Client - Sync your clipboard across devices'
    )
    parser.add_argument(
        '--user-id',
        type=int,
        required=True,
        help='Your user ID (obtained after login/registration)'
    )
    parser.add_argument(
        '--server',
        type=str,
        default='http://localhost:5000',
        help='Server URL (default: http://localhost:5000)'
    )

    args = parser.parse_args()

    print(f"Starting SyncClipboard client for user {args.user_id}")
    print(f"Connecting to server: {args.server}")
    print("Press Esc to stop the client\n")

    # Create client instance
    client = Client(user_id=args.user_id)

    # Attach server observer to send updates
    server_observer = ServerClipboardObserver(args.server)
    client.attach(server_observer)

    # Start WebSocket client to receive updates from server
    ws_client = WebSocketClipboardClient(args.server, args.user_id)

    # Connect to WebSocket in a separate thread
    ws_thread = threading.Thread(target=ws_client.connect)
    ws_thread.daemon = True
    ws_thread.start()

    print("Client is running. Monitor your clipboard!")
    print("- Copy text (Ctrl+C) to sync to server")
    print("- Paste text (Ctrl+V) to paste from local buffer")
    print("- Press Esc to quit\n")

    try:
        # Start listening for keyboard events (blocking)
        client.start_listening_debug()
    except KeyboardInterrupt:
        print("\nShutting down client...")
    finally:
        ws_client.disconnect()
        print("Client stopped")


if __name__ == "__main__":
    main()

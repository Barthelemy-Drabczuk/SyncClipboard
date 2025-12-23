# Changelog

All notable changes to SyncClipboard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 23-12-2025

### Added - Full Cross-Platform Clipboard Support 🖥️

#### Platform Improvements
- **Full Linux clipboard support** for both X11 and Wayland
  - X11 backend using `xclip` or `xsel`
  - Wayland backend using `wl-clipboard` (wl-copy/wl-paste)
  - Automatic backend detection
  - Support for both text and image clipboard operations

- **Enhanced macOS clipboard support**
  - Full image paste support using `osascript`
  - Optional `pngpaste` integration for faster operations
  - Improved reliability for image capture and paste

- **Windows clipboard improvements**
  - Optional `pywin32` for enhanced clipboard operations
  - Better error handling and fallback mechanisms

#### Architecture Refactoring
- **Renamed** `clipboard_helper.py` → `clipboard_platform.py`
- **Refactored** `ClipboardHelper` → `ClipboardPlatform` class
  - Better separation of platform-specific code
  - Singleton pattern with `get_clipboard()` function
  - Automatic platform detection on initialization
  - Individual methods for each OS: `_get_image_windows()`, `_get_image_macos()`, `_get_image_linux()`

#### Technical Implementation
- Platform detection using `platform.system()`
- Command existence checking for Linux backends
- Subprocess-based clipboard access for Linux/macOS images
- Temporary file handling for image operations
- Graceful degradation when platform tools are unavailable

#### Dependencies
- **Windows**: Optional `pywin32>=305` for enhanced support
- **macOS**: Uses built-in `osascript`, optional `pngpaste` via Homebrew
- **Linux**: Requires system packages:
  - X11: `xclip` or `xsel`
  - Wayland: `wl-clipboard`

### Changed
- Updated `Client` class to use new `clipboard_platform` module
- Improved error messages for missing platform dependencies
- Better platform-specific fallback mechanisms

### Platform Support Matrix

| Platform | Text Copy | Text Paste | Image Copy | Image Paste | Backend |
|----------|-----------|------------|------------|-------------|---------|
| Windows  | ✅ Full   | ✅ Full    | ✅ Full    | ✅ Full     | PIL + pywin32 |
| macOS    | ✅ Full   | ✅ Full    | ✅ Full    | ✅ Full     | PIL + osascript |
| Linux X11 | ✅ Full  | ✅ Full    | ✅ Full    | ✅ Full     | xclip/xsel |
| Linux Wayland | ✅ Full | ✅ Full | ✅ Full    | ✅ Full     | wl-clipboard |

### Installation Notes

#### Windows
```bash
pip install -e ".[windows]"  # Optional: for enhanced clipboard support
```

#### macOS
```bash
brew install pngpaste  # Optional: for faster clipboard operations
pip install -e ".[dev]"
```

#### Linux (X11)
```bash
sudo apt-get install xclip  # or xsel
pip install -e ".[dev]"
```

#### Linux (Wayland)
```bash
sudo apt-get install wl-clipboard
pip install -e ".[dev]"
```

---

## [0.2.0] - 23-12-2025

### Added - Image Clipboard Support 🖼️

#### Core Features
- **Image clipboard capture** using Pillow (PIL)
- **Base64 encoding** for image transmission and storage
- **Image display** in web interface with previews
- **ClipboardHelper** module for unified text and image handling
- **Cross-platform support** for Windows, macOS, and Linux

#### Technical Implementation
- Extended `ClipObject` to support both text and images
  - Added `content_type` field ("text" or "image")
  - Added `image_data` field for base64-encoded images
  - Added `from_image_bytes()` static method
  - Added `get_image_bytes()` method
  - Added `is_image()` helper method

- Created `clipboard_helper.py` module
  - `get_clipboard_content()` - Gets text or image from clipboard
  - `get_text()` - Gets text only
  - `get_image()` - Gets image and converts to ClipObject
  - `set_text()` - Sets text to clipboard
  - `set_image()` - Sets image to clipboard (platform-specific)
  - `is_image_available()` - Checks if clipboard has image

- Updated `Client` class
  - Now uses `ClipboardHelper` instead of direct `pyperclip`
  - Captures images on Ctrl+C
  - Stores `ClipObject` instances in copied buffer
  - Notifies observers with `ClipObject` instead of strings

- Updated `ClipboardObserver` pattern
  - `update()` method now receives `ClipObject`
  - `ServerClipboardObserver` sends full object data
  - Payload includes `content_type` and `image_data`

#### Server & Database
- Updated `/api/clipboard` POST endpoint
  - Accepts `content_type` and `image_data` fields
  - Broadcasts image data via WebSocket

- Updated `/api/clipboard/:user_id` GET endpoint
  - Returns `content_type` and `image_data` in history

- Enhanced `MongoCRUD.insert_transaction()`
  - Stores `content_type` and `image_data` fields
  - Supports both text and image transactions

#### Web Interface
- Updated `addClipboardItem()` function
  - Displays images as `<img>` tags with base64 data URIs
  - Shows image preview with max 300px height
  - Maintains responsive design

- WebSocket real-time updates
  - Receives and displays images instantly
  - Handles both text and image content types

#### Dependencies
- Added **Pillow >= 10.0.0** for image processing

#### Documentation
- Updated README.md with image support features
- Created comprehensive CHANGELOG.md
- Added platform compatibility notes
- Included migration guide

### Changed
- **ClipObject** now has optional parameters (backwards compatible)
- **Observer pattern** updated to pass objects instead of strings
- **Client buffer** now stores ClipObject instances
- **Database schema** extended with new fields (backwards compatible)

### Platform Support

| Platform | Image Capture | Image Paste | Status |
|----------|--------------|-------------|--------|
| Windows  | ✅ Full      | ✅ Full     | Fully Supported |
| macOS    | ✅ Full      | ⚠️ Limited  | Supported |
| Linux    | ⚠️ Limited   | ⚠️ Limited  | Partial Support |

### Known Limitations
- Images stored as base64 increase MongoDB storage by ~33%
- Linux support depends on clipboard manager
- Large images (>5MB) may impact performance
- No image compression implemented yet

---

## [0.1.0] - 22-12-2025

### Added - Initial MVP Release 🚀

#### Core Functionality
- **Text clipboard synchronization** across multiple devices
- **Real-time WebSocket updates** using Flask-SocketIO
- **Observer pattern** implementation for clipboard monitoring
- **Web interface** for viewing clipboard history
- **User authentication** system (registration and login)
- **MongoDB database** integration for persistent storage

#### Client Application
- Desktop client using `pynput` for keyboard monitoring
- Captures Ctrl+C (copy) events
- Manages clipboard buffer
- Notifies server of changes
- Press Esc to quit

#### Server Application
- Flask-based web server
- REST API endpoints:
  - `POST /api/register` - User registration
  - `POST /api/login` - User authentication
  - `POST /api/clipboard` - Add clipboard entry
  - `GET /api/clipboard/:user_id` - Get clipboard history
- WebSocket events:
  - `connect` - Client connection
  - `join` - Join user room
  - `clipboard_update` - Real-time updates

#### Web Interface
- Modern, responsive UI with gradient design
- User authentication (login/register)
- Real-time clipboard history display
- Connection status indicator
- Automatic updates via WebSocket

#### Database Layer
- **MongoCRUD** class for database operations
- CRUD operations for users and transactions
- User model with hashed passwords
- Clipboard transaction model with timestamps
- Methods for:
  - `insert_user()` - Create user
  - `insert_transaction()` - Store clipboard entry
  - `get_user()` - Authenticate user
  - `get_n_last_user_transaction()` - Retrieve history
  - `update_user()`, `update_transaction()` - Update records
  - `delete_user()`, `delete_transaction()` - Delete records

#### Models
- **ClipUser**: User model with username, password (hashed), email
- **ClipObject**: Clipboard content wrapper (text only in v0.1)

#### Development Tools
- **Docker Compose** setup for easy deployment
- **Dockerfile** for webapp containerization
- **pytest** test suite with 17 passing tests
- **pyproject.toml** for modern package management

#### Documentation
- README.md with project overview
- SETUP.md with installation instructions
- DOCKER.md with Docker deployment guide
- CONTRIBUTING.md with contribution guidelines
- TEST_RESULTS.md with test execution summary

#### Testing
- Unit tests for ClipUser and ClipObject
- Integration tests for database operations
- API endpoint tests for webapp
- All 17 tests passing

### Dependencies
- Flask 3.0.0 - Web framework
- Flask-SocketIO 5.3.5 - WebSocket support
- pymongo 4.3.3 - MongoDB integration
- pynput 1.7.6 - Keyboard monitoring
- pyperclip 1.8.2 - Clipboard access
- PyAutoGUI 0.9.53 - GUI automation
- pytest 7.2.1 - Testing framework

### Infrastructure
- MongoDB 7.0 for data storage
- Docker Compose for orchestration
- Virtual environment support
- Git version control

---

## Migration Notes

### Upgrading from 0.1.0 to 0.2.0

**Database Migration**: The database schema is backwards compatible. Existing text entries will continue to work. New fields are:
- `content_type` (defaults to "text" if missing)
- `image_data` (null for text entries)

**Client Update**: Users must update to the new client to support image capture. Old clients will still work but only capture text.

**API Compatibility**: The API is backwards compatible. Old payloads without `content_type` default to "text".

**Python Dependencies**: Run `pip install -e ".[dev]"` to install Pillow.

---

## Future Roadmap

### Planned Features

#### v0.3.0 - Enhanced Image Support
- [ ] Image compression before storage
- [ ] Thumbnail generation
- [ ] Click to view full-size images
- [ ] Download images from web interface
- [ ] Image format detection and conversion
- [ ] Size limits and validation

#### v0.4.0 - File Support
- [ ] File clipboard detection
- [ ] File upload and download
- [ ] File storage (S3/filesystem)
- [ ] File type icons
- [ ] Drag and drop upload

#### v0.5.0 - Security & Performance
- [ ] End-to-end encryption
- [ ] JWT authentication
- [ ] Secure password hashing (bcrypt)
- [ ] Rate limiting
- [ ] Image lazy loading
- [ ] Database indexing
- [ ] CDN integration

#### v1.0.0 - Production Ready
- [ ] Desktop GUI application
- [ ] Mobile apps (iOS/Android)
- [ ] Clipboard search and filtering
- [ ] Clipboard categories/tags
- [ ] Offline support with sync queue
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Keyboard shortcuts
- [ ] Clipboard item deletion
- [ ] Export/import functionality

---

## Support

For questions, bug reports, or feature requests:
- 📖 Read the [README.md](README.md)
- 🐛 Report issues on GitHub
- 💬 Join discussions
- 📧 Contact maintainers

---

**Legend:**
- ✅ Fully implemented
- ⚠️ Partially implemented
- ❌ Not implemented
- 🚀 New feature
- 🖼️ Image support
- 🔒 Security enhancement
- ⚡ Performance improvement

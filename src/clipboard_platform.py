"""
Platform-specific clipboard operations for Windows, macOS, and Linux.

Provides unified interface for clipboard access across different operating systems,
supporting both text and image content.
"""
import io
import sys
import platform
import subprocess
import tempfile
import os
from typing import Optional
from pathlib import Path

import pyperclip
from PIL import Image

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

from clip_object import ClipObject


class ClipboardPlatform:
    """Platform-specific clipboard operations handler.

    Provides cross-platform clipboard access for text and images,
    with automatic platform detection and appropriate backend selection.
    """

    def __init__(self):
        """Initialize clipboard platform handler with detected OS."""
        self.os_type = platform.system().lower()
        self._detect_linux_backend()

    def _detect_linux_backend(self) -> None:
        """Detect available clipboard backend on Linux."""
        if self.os_type != 'linux':
            return

        # Check for X11 tools
        if self._command_exists('xclip'):
            self.linux_backend = 'xclip'
        elif self._command_exists('xsel'):
            self.linux_backend = 'xsel'
        # Check for Wayland tools
        elif self._command_exists('wl-paste'):
            self.linux_backend = 'wayland'
        else:
            self.linux_backend = None

    @staticmethod
    def _command_exists(command: str) -> bool:
        """Check if a command exists in PATH."""
        try:
            subprocess.run(
                ['which', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False
            )
            return True
        except Exception:
            return False

    def get_clipboard_content(self) -> Optional[ClipObject]:
        """Get content from clipboard (text or image).

        Returns:
            Optional[ClipObject]: ClipObject with content or None if empty
        """
        # Try to get image first (images have priority)
        image = self.get_image()
        if image:
            return image

        # Fall back to text
        text = self.get_text()
        if text:
            return ClipObject(content=text, content_type="text")

        return None

    def get_text(self) -> Optional[str]:
        """Get text from clipboard.

        Returns:
            Optional[str]: Text content or None
        """
        try:
            text = pyperclip.paste()
            return text if text else None
        except Exception as e:
            print(f"Error getting text from clipboard: {e}")
            return None

    def get_image(self) -> Optional[ClipObject]:
        """Get image from clipboard using platform-specific methods.

        Returns:
            Optional[ClipObject]: ClipObject with image or None
        """
        if self.os_type == 'windows':
            return self._get_image_windows()
        elif self.os_type == 'darwin':
            return self._get_image_macos()
        elif self.os_type == 'linux':
            return self._get_image_linux()
        else:
            print(f"Unsupported OS: {self.os_type}")
            return None

    def _get_image_windows(self) -> Optional[ClipObject]:
        """Get image from Windows clipboard."""
        try:
            if ImageGrab is None:
                return None

            img = ImageGrab.grabclipboard()

            if img is None or isinstance(img, list):
                return None

            if isinstance(img, Image.Image):
                # Convert image to bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()

                return ClipObject.from_image_bytes(img_bytes, "PNG")

            return None

        except Exception as e:
            print(f"Error getting image from clipboard: {e}")
            return None

    def _get_image_macos(self) -> Optional[ClipObject]:
        """Get image from macOS clipboard using pngpaste or osascript."""
        try:
            # Try using pngpaste if available (faster and more reliable)
            if self._command_exists('pngpaste'):
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    tmp_path = tmp.name

                try:
                    result = subprocess.run(
                        ['pngpaste', tmp_path],
                        capture_output=True,
                        check=False
                    )

                    if result.returncode == 0 and os.path.exists(tmp_path):
                        with open(tmp_path, 'rb') as f:
                            img_bytes = f.read()
                        os.unlink(tmp_path)

                        if img_bytes:
                            return ClipObject.from_image_bytes(img_bytes, "PNG")
                except Exception:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)

            # Fall back to PIL ImageGrab (works on macOS)
            if ImageGrab is not None:
                img = ImageGrab.grabclipboard()

                if img and isinstance(img, Image.Image):
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='PNG')
                    img_bytes = img_byte_arr.getvalue()
                    return ClipObject.from_image_bytes(img_bytes, "PNG")

            return None

        except Exception as e:
            print(f"Error getting image from clipboard on macOS: {e}")
            return None

    def _get_image_linux(self) -> Optional[ClipObject]:
        """Get image from Linux clipboard using xclip or wl-paste."""
        if not self.linux_backend:
            print("No clipboard backend available. Install xclip, xsel, or wl-clipboard")
            return None

        try:
            if self.linux_backend == 'xclip':
                result = subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'],
                    capture_output=True,
                    check=False
                )
                if result.returncode == 0 and result.stdout:
                    return ClipObject.from_image_bytes(result.stdout, "PNG")

            elif self.linux_backend == 'xsel':
                # xsel doesn't support image clipboard directly
                # Try using xclip as fallback for images
                if self._command_exists('xclip'):
                    result = subprocess.run(
                        ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'],
                        capture_output=True,
                        check=False
                    )
                    if result.returncode == 0 and result.stdout:
                        return ClipObject.from_image_bytes(result.stdout, "PNG")

            elif self.linux_backend == 'wayland':
                result = subprocess.run(
                    ['wl-paste', '-t', 'image/png'],
                    capture_output=True,
                    check=False
                )
                if result.returncode == 0 and result.stdout:
                    return ClipObject.from_image_bytes(result.stdout, "PNG")

            return None

        except Exception as e:
            print(f"Error getting image from clipboard on Linux: {e}")
            return None

    def set_text(self, text: str) -> bool:
        """Set text to clipboard.

        Args:
            text (str): Text to set

        Returns:
            bool: True if successful
        """
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Error setting text to clipboard: {e}")
            return False

    def set_image(self, clip_object: ClipObject) -> bool:
        """Set image to clipboard using platform-specific methods.

        Args:
            clip_object (ClipObject): ClipObject with image data

        Returns:
            bool: True if successful
        """
        if not clip_object.is_image():
            return False

        if self.os_type == 'windows':
            return self._set_image_windows(clip_object)
        elif self.os_type == 'darwin':
            return self._set_image_macos(clip_object)
        elif self.os_type == 'linux':
            return self._set_image_linux(clip_object)
        else:
            print(f"Unsupported OS for image clipboard: {self.os_type}")
            return False

    def _set_image_windows(self, clip_object: ClipObject) -> bool:
        """Set image to Windows clipboard."""
        try:
            img_bytes = clip_object.get_image_bytes()
            if not img_bytes:
                return False

            # Convert bytes to PIL Image
            img = Image.open(io.BytesIO(img_bytes))

            # Use win32clipboard if available
            try:
                import win32clipboard
                from io import BytesIO

                output = BytesIO()
                img.convert('RGB').save(output, 'BMP')
                data = output.getvalue()[14:]  # Remove BMP header
                output.close()

                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                return True

            except ImportError:
                print("win32clipboard not available. Install pywin32 for full Windows support.")
                return False

        except Exception as e:
            print(f"Error setting image to clipboard on Windows: {e}")
            return False

    def _set_image_macos(self, clip_object: ClipObject) -> bool:
        """Set image to macOS clipboard using osascript."""
        try:
            img_bytes = clip_object.get_image_bytes()
            if not img_bytes:
                return False

            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp.write(img_bytes)
                tmp_path = tmp.name

            try:
                # Use osascript to set clipboard
                script = f'''
                set the clipboard to (read (POSIX file "{tmp_path}") as «class PNGf»)
                '''
                result = subprocess.run(
                    ['osascript', '-e', script],
                    capture_output=True,
                    check=False
                )

                os.unlink(tmp_path)
                return result.returncode == 0

            except Exception:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                return False

        except Exception as e:
            print(f"Error setting image to clipboard on macOS: {e}")
            return False

    def _set_image_linux(self, clip_object: ClipObject) -> bool:
        """Set image to Linux clipboard using xclip or wl-copy."""
        if not self.linux_backend:
            print("No clipboard backend available. Install xclip, xsel, or wl-clipboard")
            return False

        try:
            img_bytes = clip_object.get_image_bytes()
            if not img_bytes:
                return False

            if self.linux_backend == 'xclip':
                result = subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i'],
                    input=img_bytes,
                    check=False
                )
                return result.returncode == 0

            elif self.linux_backend == 'xsel':
                # xsel doesn't support images directly, use xclip if available
                if self._command_exists('xclip'):
                    result = subprocess.run(
                        ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i'],
                        input=img_bytes,
                        check=False
                    )
                    return result.returncode == 0
                else:
                    print("Image clipboard requires xclip on Linux with xsel backend")
                    return False

            elif self.linux_backend == 'wayland':
                result = subprocess.run(
                    ['wl-copy', '-t', 'image/png'],
                    input=img_bytes,
                    check=False
                )
                return result.returncode == 0

            return False

        except Exception as e:
            print(f"Error setting image to clipboard on Linux: {e}")
            return False

    def is_image_available(self) -> bool:
        """Check if clipboard contains an image.

        Returns:
            bool: True if image is available
        """
        try:
            if self.os_type == 'windows' or self.os_type == 'darwin':
                if ImageGrab is not None:
                    img = ImageGrab.grabclipboard()
                    return isinstance(img, Image.Image)
                return False

            elif self.os_type == 'linux':
                if not self.linux_backend:
                    return False

                if self.linux_backend in ['xclip', 'xsel']:
                    # Check if clipboard has image/png target
                    result = subprocess.run(
                        ['xclip', '-selection', 'clipboard', '-t', 'TARGETS', '-o'],
                        capture_output=True,
                        check=False
                    )
                    return b'image/png' in result.stdout

                elif self.linux_backend == 'wayland':
                    result = subprocess.run(
                        ['wl-paste', '--list-types'],
                        capture_output=True,
                        check=False
                    )
                    return b'image/png' in result.stdout

            return False

        except Exception:
            return False


# Singleton instance for convenience
_clipboard = None


def get_clipboard() -> ClipboardPlatform:
    """Get singleton clipboard instance.

    Returns:
        ClipboardPlatform: The clipboard platform handler
    """
    global _clipboard
    if _clipboard is None:
        _clipboard = ClipboardPlatform()
    return _clipboard

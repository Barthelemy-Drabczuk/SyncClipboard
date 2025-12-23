import base64
from typing import Optional


class ClipObject:
    """Represents a clipboard item (text or image)"""

    def __init__(
        self,
        content: str,
        content_type: str = "text",
        image_data: Optional[str] = None
    ) -> None:
        """Initialize a clipboard object

        Args:
            content (str): Text content or image description
            content_type (str): Either "text" or "image"
            image_data (str): Base64 encoded image data (if content_type is "image")
        """
        self.content = content
        self.content_type = content_type
        self.image_data = image_data

    def to_json(self) -> dict:
        """Convert to JSON-serializable dict

        Returns:
            dict: Dictionary representation
        """
        return {
            "content": self.content,
            "content_type": self.content_type,
            "image_data": self.image_data
        }

    def get_content(self) -> str:
        """Get the text content

        Returns:
            str: The content
        """
        return self.content

    def get_content_type(self) -> str:
        """Get the content type

        Returns:
            str: Either "text" or "image"
        """
        return self.content_type

    def get_image_data(self) -> Optional[str]:
        """Get the base64 encoded image data

        Returns:
            Optional[str]: Base64 encoded image or None
        """
        return self.image_data

    def is_image(self) -> bool:
        """Check if this is an image clip

        Returns:
            bool: True if image, False if text
        """
        return self.content_type == "image"

    @staticmethod
    def from_image_bytes(image_bytes: bytes, image_format: str = "PNG") -> 'ClipObject':
        """Create a ClipObject from image bytes

        Args:
            image_bytes (bytes): Raw image data
            image_format (str): Image format (PNG, JPEG, etc.)

        Returns:
            ClipObject: New clipboard object with image
        """
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        return ClipObject(
            content=f"Image ({image_format})",
            content_type="image",
            image_data=image_b64
        )

    def get_image_bytes(self) -> Optional[bytes]:
        """Get the image as bytes

        Returns:
            Optional[bytes]: Decoded image bytes or None
        """
        if self.image_data:
            return base64.b64decode(self.image_data)
        return None

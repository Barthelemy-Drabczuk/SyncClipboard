from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from clip_object import ClipObject


class ClipboardObserver(ABC):
    """Abstract observer interface for clipboard changes"""

    @abstractmethod
    def update(self, user_id: int, clip_obj: 'ClipObject') -> None:
        """Called when clipboard content changes

        Args:
            user_id (int): The user ID who made the change
            clip_obj (ClipObject): The clipboard object (text or image)
        """
        pass


class ClipboardSubject:
    """Subject that notifies observers of clipboard changes"""

    def __init__(self):
        self._observers: List[ClipboardObserver] = []

    def attach(self, observer: ClipboardObserver) -> None:
        """Attach an observer

        Args:
            observer (ClipboardObserver): Observer to attach
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: ClipboardObserver) -> None:
        """Detach an observer

        Args:
            observer (ClipboardObserver): Observer to detach
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, user_id: int, clip_obj: 'ClipObject') -> None:
        """Notify all observers of a clipboard change

        Args:
            user_id (int): The user ID who made the change
            clip_obj (ClipObject): The clipboard object (text or image)
        """
        for observer in self._observers:
            observer.update(user_id, clip_obj)


class ServerClipboardObserver(ClipboardObserver):
    """Observer that sends clipboard updates to the server"""

    def __init__(self, server_url: str):
        """Initialize the server observer

        Args:
            server_url (str): The URL of the server API
        """
        self.server_url = server_url

    def update(self, user_id: int, clip_obj: 'ClipObject') -> None:
        """Send clipboard update to server

        Args:
            user_id (int): The user ID who made the change
            clip_obj (ClipObject): The clipboard object (text or image)
        """
        import requests
        try:
            # Send clipboard data to server
            payload = {
                "user_id": user_id,
                "content": clip_obj.get_content(),
                "content_type": clip_obj.get_content_type(),
                "image_data": clip_obj.get_image_data()
            }

            response = requests.post(
                f"{self.server_url}/api/clipboard",
                json=payload
            )

            if response.status_code == 200:
                content_type = clip_obj.get_content_type()
                print(f"Clipboard {content_type} sent to server successfully")
            else:
                print(f"Failed to send clipboard: {response.status_code}")
        except Exception as e:
            print(f"Error sending clipboard to server: {e}")

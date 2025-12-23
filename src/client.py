import signal
import pyperclip
import pyautogui as pgui
from pynput.keyboard import Key, Listener, KeyCode
from clipboard_observer import ClipboardSubject
from clipboard_platform import get_clipboard
from clip_object import ClipObject


class Client(ClipboardSubject):
    """Client that monitors clipboard and notifies observers of changes"""

    def __init__(self, user_id: int = None) -> None:
        """Initialize the client

        Args:
            user_id (int): The ID of the logged-in user
        """
        super().__init__()
        self.user_id = user_id
        self.pressed_keys: list[Key] = list()
        self.copied_stuff: list[str] = list()
        self.pasted_stuff: list[str] = list()
        self.clipboard = get_clipboard()  # Get singleton clipboard instance
        self.listener = Listener(
            on_press=self.__on_press,
            on_release=self.__on_release
        )
        signal.signal(signal.SIGINT, self.__intercept)

    def __on_press(self, key: Key) -> None:
        """Handle key press events

        Args:
            key (Key): The key that was pressed
        """
        print(f"__on_press - key: {key}")
        if key == Key.ctrl or Key.ctrl in self.get_read_buffer():
            self.pressed_keys.append(key)
            print(
                f"__on_press - read buffer: {self.get_read_buffer()}"
            )
            if KeyCode.from_char('c') in self.get_read_buffer():
                # Get clipboard content (text or image)
                clip_obj = self.clipboard.get_clipboard_content()

                if clip_obj:
                    # Store in buffer
                    self.copied_stuff.append(clip_obj)
                    print(
                        f"__on_press - copied {clip_obj.get_content_type()}: "
                        f"{clip_obj.get_content()[:50] if len(clip_obj.get_content()) > 50 else clip_obj.get_content()}"
                    )

                    # Notify observers if user is logged in
                    if self.user_id is not None:
                        self.notify(self.user_id, clip_obj)
            elif KeyCode.from_char('v') in self.get_read_buffer():
                if len(self.get_copied_buffer()) != 0:
                    pasting: str = pyperclip.copy(
                        self.get_copied_buffer()[-1]
                    )
                    pgui.write(pasting)
                    self.pasted_stuff.append(
                        self.get_copied_buffer()[-1]
                    )
                    print(
                        f"__on_press - pasted buffer with copy: "
                        f"{self.pasted_stuff}"
                    )
                else:
                    pyperclip.copy('')
                    pgui.write('')
                    self.pasted_stuff.append('')
                    print(
                        f"__on_press - pasted buffer without copy: "
                        f"{self.pasted_stuff}"
                    )

    def __on_release(self, key: Key) -> bool:
        """Handle key release events

        Args:
            key (Key): The key that was released

        Returns:
            bool: False to stop listener, None to continue
        """
        print(f"__on_release - key: {key}")
        if key != KeyCode.from_char('c') or \
           key != KeyCode.from_char('v'):
            self.get_read_buffer().clear()
        print(
            f"__on_release - read buffer: "
            f"{self.get_read_buffer()}"
        )
        if key == Key.esc:
            return False

    def __intercept(*args) -> None:
        """Intercept SIGINT signal"""
        pass

    def __get_listener(self) -> Listener:
        """Get the keyboard listener

        Returns:
            Listener: The keyboard listener instance
        """
        return self.listener

    def start_listening(self) -> None:
        """Start the keyboard listener in the background"""
        self.__get_listener().start()

    def start_listening_debug(self) -> None:
        """Start the keyboard listener in debug mode (blocking)"""
        with Listener(
            on_press=self.__on_press,
            on_release=self.__on_release
        ) as listener:
            listener.join()

    def get_read_buffer(self) -> list[Key]:
        """Get the current key buffer

        Returns:
            list[Key]: List of currently pressed keys
        """
        return self.pressed_keys

    def get_copied_buffer(self) -> list[str]:
        """Get the copied content buffer

        Returns:
            list[str]: List of copied content
        """
        return self.copied_stuff

    def get_pasted_buffer(self) -> list[str]:
        """Get the pasted content buffer

        Returns:
            list[str]: List of pasted content
        """
        return self.pasted_stuff


if __name__ == "__main__":
    client = Client()
    client.start_listening_debug()

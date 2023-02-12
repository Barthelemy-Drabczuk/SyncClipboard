import signal
import pyperclip
from pynput.keyboard import Key, Listener, KeyCode


class Client:
    """_summary_
    """
    def __init__(self) -> None:
        """_summary_
        """
        self.pressed_keys: list[Key] = list()
        self.copied_stuff: list[str] = list()
        self.pasted_stuff: list[str] = list()
        self.listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        signal.signal(signal.SIGINT, self.__intercept)
    
    def __on_press(self, key: Key) -> None:
        """_summary_

        Args:
            key (Key): _description_
        """
        print(f"__on_press - key: {key}")
        if key == Key.ctrl or Key.ctrl in self.get_read_buffer():
            self.pressed_keys.append(key)
            print(f"__on_press - read buffer: {self.get_read_buffer()}")
            if KeyCode.from_char('c') in self.get_read_buffer():
                self.copied_stuff.append(pyperclip.paste())
                print(f"__on_press - copied buffer: {self.get_copied_buffer()}")
            elif KeyCode.from_char('v') in self.get_read_buffer():
                if len(self.get_copied_buffer()) != 0:
                    pyperclip.copy(self.get_copied_buffer()[-1])
                    pyperclip.paste()
                    self.pasted_stuff.append(self.get_copied_buffer()[-1])
                    print(f"__on_press - pasted buffer with copy: {self.pasted_stuff}")
                else:
                    pyperclip.copy('')
                    pyperclip.paste()
                    self.pasted_stuff.append('')
                    print(f"__on_press - pasted buffer without copy: {self.pasted_stuff}")


    def __on_release(self, key: Key) -> bool:
        """_summary_

        Args:
            key (Key): _description_

        Returns:
            bool: _description_
        """
        print(f"__on_release - key: {key}")
        if key != KeyCode.from_char('c') or key != KeyCode.from_char('v'):
            self.get_read_buffer().clear()
        print(f"__on_release - read buffer: {self.get_read_buffer()}")
        if key == Key.esc:
            return False


    def __intercept(*args) -> None:
        """_summary_
        """
        pass


    def __get_listener(self) -> Listener:
        """_summary_

        Returns:
            Listener: _description_
        """
        return self.listener


    def start_listening(self) -> None:
        """_summary_
        """
        self.__get_listener().start()


    def start_listening_debug(self) -> None:
        """_summary_
        """
        with Listener(on_press=self.__on_press, on_release=self.__on_release) as listener:
            listener.join()


    def get_read_buffer(self) -> list[Key]:
        """_summary_

        Returns:
            list[Key]: _description_
        """
        return self.pressed_keys
    

    def get_copied_buffer(self) -> list[str]:
        """_summary_

        Returns:
            list[str]: _description_
        """
        return self.copied_stuff

    
    def get_pasted_buffer(self) -> list[str]:
        """_summary_

        Returns:
            list[str]: _description_
        """
        return self.pasted_stuff


if __name__ == "__main__":
    client = Client()
    client.start_listening_debug()

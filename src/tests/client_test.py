import time

import pytest
import pyautogui as pgui

from pynput.keyboard import Key, Listener, KeyCode, Controller

from client import Client


keyboard = Controller()

def test_keyboard_input_recongnition():
    client_input = Client()
    client_input.start_listening()
    time.sleep(0.1)
    pgui.write('azerty\n')
    
    assert len(client_input.get_read_buffer()) == 0

    client_input.get_read_buffer().clear()
    keyboard.press(Key.ctrl)
    keyboard.press('c')

    assert len(client_input.get_read_buffer()) >= 2

    keyboard.release(Key.ctrl)
    keyboard.release('c')



def test_copied_inputs():
    client_copied = Client()
    client_copied.start_listening()

    keyboard.press(Key.ctrl)
    keyboard.press('c')

    assert len(client_copied.get_copied_buffer()) != 0

    keyboard.release(Key.ctrl)
    keyboard.release('c')


def test_pasted_outputs():
    client_paste = Client()
    client_paste.start_listening()

    keyboard.press(Key.ctrl)
    keyboard.press('v')

    assert len(client_paste.get_pasted_buffer()) != 0

    keyboard.release(Key.ctrl)
    keyboard.release('v')
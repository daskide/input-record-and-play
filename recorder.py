#!/usr/bin/env python3

# General-purpose dependencies
from enum import Enum
import time
import json
import sys
import argparse
# Record dependencies
from pynput import mouse
from pynput import keyboard
# Play dependencies
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from entities import InputType, MouseAction, KeyboardAction, Button as MB


def create_mouse_action(timestamp, action, button, x, y):
    return {
        'input_type': InputType.MOUSE,
        'timestamp': timestamp,
        'data': {
            'action': action,
            'button': button,
            'position': (x, y)
        }
    }

def create_keyboard_action(timestamp, action, key):
    return {
        'input_type': InputType.KEYBOARD,
        'timestamp': timestamp,
        'data': {
            'action': action,
            'key': key,
        }
    }


class MyException(Exception): pass


class Recorder():
    def __init__(self):
        self.actions = []
        self.start_time = 0

    def _format_actions(self):
        return {'actions': self.actions}

    def _get_time_since_start(self):
        return time.time() - self.start_time# * 1000 - self.start_time

    def _on_move(self, x, y):
        #print('Pointer moved to {0}'.format((x, y)))
        self.actions.append(create_mouse_action(self._get_time_since_start(), MouseAction.MOVED, None, x, y))

    def _format_button_enum(self, button):
        # this method is used to convert a pynput.mouse.Button enum to
        # Button(int, enum), which can be dumped to json as int
        return MB(button.value)

    def _on_click(self, x, y, button, pressed):
        #print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        action = MouseAction.PRESSED if pressed else MouseAction.RELEASED 
        button = self._format_button_enum(button)
        self.actions.append(create_mouse_action(self._get_time_since_start(), action, button.value(), x, y))

    def _on_scroll(self, x, y, dx, dy):
        return
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))
        
    def _on_press(self, key):
        self.actions.append(create_keyboard_action(self._get_time_since_start(), KeyboardAction.PRESSED, key.value()))
        # try:
        #     print('alphanumeric key {0} pressed'.format(key.char))
        # except AttributeError:
        #     print('special key {0} pressed'.format(key))

    def _on_release(self, key):
        self.actions.append(create_keyboard_action(self._get_time_since_start(), KeyboardAction.RELEASED, key.value()))
        # print('{0} released'.format(key))
        # if key == keyboard.Key.esc:
        #     # Stop listener
        #     return False

    def _create_new_listeners(self):
        self.mouse_listener = mouse.Listener(
                on_move=self._on_move,
                on_click=self._on_click,
                on_scroll=self._on_scroll)
        
        self.keyboard_listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release)

    def get_actions(self):
        return self.actions
    
    def on_activate_pause(self):
        print('<ctrl>+<alt>+p pressed')
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def on_activate_start(self):
        print('<ctrl>+<alt>+o pressed')
        if not self.mouse_listener.is_alive():
            self._create_new_listeners()
            self.mouse_listener.start()
            self.keyboard_listener.start()

    def on_activate_finish(self):
        print('<ctrl>+<alt>+w pressed')
        if self.mouse_listener.is_alive():
            mouse.Listener.stop(self.mouse_listener)
            keyboard.Listener.stop(self.keyboard_listener)
        raise MyException("Application stopped")

    def record(self):
        self.start_time = time.time()# * 1000
        self._create_new_listeners()

        # hot_keys_listener = keyboard.GlobalHotKeys({
        #     '<ctrl>+<alt>+o': self.on_activate_start,
        #     '<ctrl>+<alt>+p': self.on_activate_pause,
        #     '<ctrl>+<alt>+w': self.on_activate_finish})
        
        # hot_keys_listener.start()
        # hot_keys_listener.join()

        with keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+o': self.on_activate_start,
            '<ctrl>+<alt>+p': self.on_activate_pause,
            '<ctrl>+<alt>+w': self.on_activate_finish}) as hot_keys_listener:
            try:
                hot_keys_listener.join()
            except MyException as e:
                print('{0} was pressed'.format(e.args[0]))
# hot_keys_listener.start()
        #mouse_listener.join()
        
        #keyboard.GlobalHotKeys.stop(hot_keys_listener)

        return self._format_actions()

        # # ...or, in a non-blocking fashion:
        # listener = mouse.Listener(
        #     on_move=on_move,
        #     on_click=on_click,
        #     on_scroll=on_scroll)
        # listener.start()

        # Collect events until released
        # with mouse.Listener(
        #         on_move=self._on_move,
        #         on_click=self._on_click,
        #         on_scroll=self._on_scroll) as mouse_listener:
        #     mouse_listener.join()
        
        # with keyboard.Listener(
        # on_press=self._on_press,
        # on_release=self._on_release) as keyboard_listener:
        #     keyboard_listener.join()


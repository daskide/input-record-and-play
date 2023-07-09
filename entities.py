#!/usr/bin/env python3
from enum import Enum
from pynput.mouse import Button as MouseButton

class InputType(int, Enum):
    MOUSE = 1
    KEYBOARD = 2


class MouseAction(int, Enum):
    PRESSED = 1
    RELEASED = 2
    MOVED = 3
    SCROLLED = 4


class KeyboardAction(int, Enum):
    PRESSED = 1
    RELEASED = 2


class Button(int, Enum):
    unknown = 0
    left = 1
    middle = 2
    right = 3
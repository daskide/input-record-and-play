#!/usr/bin/env python3

# General-purpose dependencies
from enum import Enum
import time
from threading import Timer
import json
import sys
import argparse
# Record dependencies
from pynput import mouse
from pynput import keyboard
# Play dependencies
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from entities import InputType, MouseAction, KeyboardAction


class Player():
    def __init__(self, recordings, number_of_repeats):
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()
        self.number_of_repeats = number_of_repeats
        self.recordings = recordings
        for recording in recordings:
            self._calculate_actions_duration(recording['actions'])

    def _handle_mouse_action(self, data):
        if data['action'] == MouseAction.PRESSED:
            self.mouse_controller.press(Button(data['button']))
        elif data['action'] == MouseAction.RELEASED:
            self.mouse_controller.release(Button(data['button']))
        elif data['action'] == MouseAction.MOVED:
            #self.mouse_controller.move(*action['position'])
            self.mouse_controller.position = data['position']
        #elif data['action'] == MouseAction.SCROLLED:
            #self.mouse_controller.scroll(*data['position'])

    def _handle_keyboard_action(self, data):
        if data['action'] == KeyboardAction.PRESSED:
            self.keyboard_controller.press(Key(data['key']))
        elif data['action'] == KeyboardAction.RELEASED:
            self.keyboard_controller.release(Key(data['key']))

    def _calculate_actions_duration(self, actions):
        for i in range(len(actions) - 1):
            actions[i]['duration'] = actions[i+1]['timestamp'] - actions[i]['timestamp']
            actions[i]['next_timestamp'] = actions[i+1]['timestamp']
        actions[len(actions) - 1]['duration'] = 0
        actions[len(actions) - 1]['next_timestamp'] = actions[len(actions) - 2]['timestamp'] + 0.5

    def _handle_action(self, action):
            if action['input_type'] == InputType.MOUSE:
                self._handle_mouse_action(action['data'])
            elif action['input_type'] == InputType.KEYBOARD:
                self._handle_keyboard_action(action['data'])
            else:
                print('Unknown input type {0}'.format(action['input_type']))

    def start_playing_recordings(self):
        for _ in range(self.number_of_repeats):
            for recording in self.recordings:
                for _ in range(recording['repeats']):
                    self.start_playing(recording['actions'])

    def start_playing(self, actions):
        start_time = time.time()
        for action in actions:
            while(action['next_timestamp'] > time.time() - start_time):
                time.sleep(0.0001)
            self._handle_action(action)
            


#!/usr/bin/env python3

# General-purpose dependencies
import json
import sys
import argparse
# Record dependencies
from pynput import keyboard
# Play dependencies
from pynput.keyboard import Key, Controller as KeyboardController

from recorder import Recorder
from player import Player
from file_manager import FileManager

import ctypes


PROCESS_PER_MONITOR_DPI_AWARE = 2

ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

def handle_recording(args):
    fm = FileManager()
    fm.check_path_is_correct(args.filename)

    rec = Recorder()
    actions = rec.record()
    fm.save_to_file(args.filename, actions)

def handle_playing(args):
    fm = FileManager()
    fm.check_files_exist(args.filenames)
    recordings = []
    for filename in args.filenames:
        recordings.append(fm.load_from_file(filename))
    for idx, recording in enumerate(recordings):
        recording['repeats'] = args.individual_repeats[idx]   

    player = Player(recordings, number_of_repeats=args.repeats)
    player.start_playing_recordings()

def parse_args():
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', required=True) #required=True

    recorder = subparsers.add_parser('record', help='help')
    recorder.add_argument('filename', help='destination file of input recording')
    recorder.set_defaults(func=handle_recording)

    player = subparsers.add_parser('play', help='help')
    player.add_argument('filenames', nargs='+', help='source files of recordings to be played')
    player.add_argument('-i', '--individual-repeats', nargs='*', help='number of times to repeat individual recording', default=[1])
    player.add_argument('-r', '--repeats', nargs='*', help='number of times to repeat sequence of recordings', default=1)
    player.set_defaults(func=handle_playing)

    args = parser.parse_args()
    args.func(args)

def main():
    parse_args()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

"""
102624
Support Functions for the QuakePy Compiler
"""

import json
import platform
import subprocess

from tkinter.constants import *

import tkinter.font as tkf

def readConfig(file):
    """
    Read json file to be used as config info.
    :param file:
    :return:
    """
    try:
        with open(file) as in_file:
            config = json.load(in_file)
    except Exception as err:
        return err
    return config

def writeConfig(file, json_str):
    """
    Write json file data to be used as config info.
    :param file:
    :param json_str:
    :return:
    """
    try:
        with open(file, 'w') as out_file:
            json.dump(json_str, out_file, indent=4)
    except Exception as err:
        return err
    return True

def widthForWidget(txt):
    """
    Calculate the width of the widget based on the length of the string and font.
    :param txt: String
    :return: Int to be used for the width of the widget.
    """
    opsys = platform.system()
    if opsys == 'Windows': divisor = 8
    elif opsys == 'Darwin': divisor = 9

    str_len = tkf.Font().measure(text=txt)
    return int(str_len / divisor)

def launch(text_widget, command, cls=False):
    """
    Subprocess Function to Launch the ericw tools and Quake
    :param text_widget: tk.Text widget object to display subprocess information.
    :param command: List of commands and arguments.
    :param cls: Option to clear the tk.Text widget before new text is displayed.
    :return:
    """
    text_widget['state'] = NORMAL
    if cls: text_widget.delete('1.0', END)

    p = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    pid = p.pid
    stdout, stderr = p.communicate()
    if stderr:
        text_widget.insert(END, stderr)
    elif stdout:
        text_widget.insert(END, stdout)

    text_widget.insert(END, f"\n *** Process Finished with Exit Code: {p.returncode} ***\n\n")
    text_widget['state'] = DISABLED

    return p

#!/usr/bin/env python3

"""
102924
First run configuration app to create a config file (config.json) for the QuakePy Compiler.
"""

import os
import tkinter as tk
import tkinter.filedialog as tfd
import tkinter.messagebox as tmb
import tkinter.font as tkf
from tkinter.constants import *

import foo

BTNWIDTH = 1
CONFIGFILE = "config.json"
CONFIGTITLE = "QuakePy Compiler Config"
SETTINGS = "dev_map", "tool_bin", "id_folder", "dev_folder", "quake_engine", "engine_arg"
OPTIONS = "qbsp_opt", "vis_opt", "light_opt"
DFLTENGARG = "-basedir <DEVFLDR> +map <DEVMAP>"

class firstRunDialog(tk.Tk):
    """
    First run to build the config.json file.
    """
    def __init__(self):
        super().__init__()
        self.title(CONFIGTITLE)
        self.resizable(width=True, height=False)

        self.app_config = dict()
        self.settingStrVar = {set:tk.StringVar() for set in SETTINGS}  # Dict of tk.StringVar. Key = settings, value = tk.StringVar.
        self.toolOptStrVar = {opt:tk.StringVar() for opt in OPTIONS}

        self.settingStrVar['engine_arg'].set(DFLTENGARG)

        widget_width = int(max([tkf.Font().measure(text=self.settingStrVar[s].get()) for s in SETTINGS]) / 8.5)

        dlgFrame = tk.Frame(self)
        dlgFrame.pack(expand=True, fill=X, pady=5, padx=5)

        configFrame = tk.Frame(dlgFrame)
        configFrame.columnconfigure(index=1, weight=1)
        configFrame.pack(fill=X)

        devLabel = tk.Label(configFrame, text="Dev Folder:")
        devLabel.grid(row=0, column=0, sticky=E)
        devEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['dev_folder'])
        devEntry.grid(row=0, column=1, sticky=EW, pady=5, padx=5)
        devButton = tk.Button(configFrame, width=BTNWIDTH, text="...",
                              command=lambda: self.processFolderChange('dev_folder'))
        devButton.grid(row=0, column=2, sticky=E)

        toolLabel = tk.Label(configFrame, text="Tool Bin:")
        toolLabel.grid(row=1, column=0, sticky=E)
        toolEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['tool_bin'])
        toolEntry.grid(row=1, column=1, sticky=EW, pady=5, padx=5)
        toolButton = tk.Button(configFrame, width=BTNWIDTH, text="...",
                               command=lambda: self.processFolderChange('tool_bin'))
        toolButton.grid(row=1, column=2, sticky=E)

        engineLabel = tk.Label(configFrame, text="Quake Engine:")
        engineLabel.grid(row=2, column=0, sticky=E)
        engineEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['quake_engine'])
        engineEntry.grid(row=2, column=1, sticky=EW, pady=5, padx=5)
        engineButton = tk.Button(configFrame, width=BTNWIDTH, text="...",
                                 command=lambda: self.processFileChange('quake_engine'))
        engineButton.grid(row=2, column=2, sticky=E)

        argumentsLabel = tk.Label(configFrame, text="Arguments:")
        argumentsLabel.grid(row=3, column=0, sticky=E)
        argumentsEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['engine_arg'])
        argumentsEntry.grid(row=3, column=1, sticky=EW, pady=5, padx=5)
        argumentsButton = tk.Button(configFrame, width=BTNWIDTH, text="?",
                                    command=lambda: self.processFolderChange('engine_arg'))
        argumentsButton.grid(row=3, column=2, sticky=E)

        idLabel = tk.Label(configFrame, text="id Folder:")
        idLabel.grid(row=4, column=0, sticky=E)
        idEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['id_folder'])
        idEntry.grid(row=4, column=1, sticky=EW, pady=5, padx=5)
        idButton = tk.Button(configFrame, width=BTNWIDTH, text="...",
                             command=lambda: self.processFolderChange('id_folder'))
        idButton.grid(row=4, column=2, sticky=E)

        buttonFrame = tk.Frame(dlgFrame)
        buttonFrame.columnconfigure(index=0, weight=1)
        buttonFrame.pack(fill=X)
        labels = "Save", "Cancel"
        btn_width = max([len(l) for l in labels])

        saveButton = tk.Button(buttonFrame, width=btn_width, text="Save",
                               command=self.saveConfig)
        saveButton.grid(row=0, column=0, sticky=E, pady=5, padx=5)

        cancelButton = tk.Button(buttonFrame, width=btn_width, text="Cancel",
                                 command=self.destroy)
        cancelButton.grid(row=0, column=1, sticky=E, pady=5, padx=5)

        self.update_idletasks()
        win_width = self.winfo_width()
        win_height = self.winfo_height()
        self.minsize(width=win_width, height=win_height)
        self.mainloop()

    def processFileChange(self, event):
        if event == 'dev_map':
            initdir = os.path.split(self.settingStrVar['dev_map'].get())[0]
        else:
            initdir = self.settingStrVar['dev_folder'].get()
        file = tfd.askopenfilename(initialdir=initdir)
        if file:
            self.settingStrVar[event].set(file)

    def processFolderChange(self, event):
        fldr = tfd.askdirectory(initialdir=self.settingStrVar['dev_folder'].get())
        if fldr:
            self.settingStrVar[event].set(fldr)

    def saveConfig(self):
        config_comp = 0
        self.app_config['dev_map'] = self.settingStrVar['dev_map'].get()
        for s in SETTINGS:
            if s != 'dev_map':
                self.app_config[s] = self.settingStrVar[s].get()
                if self.app_config[s]:
                    config_comp += 1
                else:
                    tmb.showerror("ERROR!", "Missing Config Info!")
                    break
        if config_comp == 5:
            for o in OPTIONS:
                self.app_config[o] = ""
            foo.writeConfig(CONFIGFILE, self.app_config)
            tmb.showinfo("Success!", "Config Complete, QuakePy Compiler will now Start!")
            self.destroy()


if __name__ == '__main__':
    firstRunDialog()

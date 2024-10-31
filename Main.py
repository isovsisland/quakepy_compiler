#!/usr/bin/env python3

"""
102624
QuakePy Compiler
For use with ericw-tools to compile Quake maps. https://ericwa.github.io/ericw-tools/
Similar to and inspired by necros compiling GUI. https://github.com/necros0/ne_q1CompilingGui
To be used in conjunction with TrenchBroom https://trenchbroom.github.io/

Favorite Quake Ports
vkQuake https://github.com/Novum/vkQuake/releases/tag/1.31.2  - My Favorite but No Longer in Development!
& vkQuake-RT for truly spectacular Quake ray traced visuals!
IronWail https://github.com/andrei-drexler/ironwail/releases  - A close 2nd to vkQuake but will probably end up being my goto.
QuakeSpasm https://sourceforge.net/projects/quakespasm/  - Support for Mac Machines - Yea!

TODO: Add Hovertips.
TODO: Add Quake engine help.
TODO: Add app icon.
TODO: Add About dialog.
"""

import os
import shutil
import platform

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkf
import tkinter.filedialog as tfd
import tkinter.messagebox as tmb
from tkinter.constants import *

import foo
import firstRunDialog as frd

BTNWIDTH = 1
TITLE = "QuakePy Compiler"
CONFIGFILE = "config.json"
DFLTENGARG = "-basedir <DEVFLDR> +map <DEVMAP>"
SETTINGS = "dev_map", "tool_bin", "id_folder", "dev_folder", "quake_engine", "engine_arg"
OPTIONS = "qbsp_opt", "vis_opt", "light_opt"
TOOLS = "qbsp", "vis", "light"
MAC_PREFIX = ["open", "-a"]
MAC_SUFFIX = ["--args"]


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self.resizable(width=True, height=False)
        self.opsys = platform.system()
        self.font = tkf.Font(self).actual()
        self.protocol('WM_DELETE_WINDOW', lambda: self.processUI('quit'))

        self.app_config = foo.readConfig(CONFIGFILE)
        if isinstance(self.app_config, FileNotFoundError):  # Exception
            tmb.showerror("Error!", "Please Restart the App and Fill in the Config Dialog.")
            return

        if self.app_config['engine_arg'] == "":
            self.app_config['engine_arg'] = DFLTENGARG

        self.settingStrVar = {ky:tk.StringVar() for ky in SETTINGS}  # Dict of tk.StringVar. Key = settings, value = tk.StringVar.
        [self.settingStrVar[ky].set(self.app_config[ky]) for ky in SETTINGS]  # Set tk.Entry values with paths from config file.

        self.toolOptStrVar = {ky:tk.StringVar() for ky in OPTIONS}
        [self.toolOptStrVar[ky].set(self.app_config[ky]) for ky in OPTIONS]

        # OS Specific Formatting for Executable Binaries #
        if  self.opsys == 'Windows':
            tool_bin = "qbsp.exe", "vis.exe", "light.exe"
        elif self.opsys == 'Darwin':
            tool_bin = "qbsp", "vis", "light"
        self.toolPath = {TOOLS[x]:os.path.join(self.app_config['tool_bin'], t) for x, t in enumerate(tool_bin)}  # Dict to tool paths.

        rootFrame = tk.Frame(self)
        rootFrame.pack(expand=True, fill=BOTH, pady=5, padx=5)

        # Widget Groups #
        self.menuGroup()
        self.mapGroup(rootFrame)
        self.compileGroup(rootFrame)
        self.resultText = self.resultGroup(rootFrame)
        self.buttonGroup(rootFrame)

        # Set Minimum Size, Center the Window & Start Main Loop #
        self.update_idletasks()  # Update widgets to get accurate sizes.
        win_width = self.winfo_width()
        win_height = self.winfo_height()
        self.minsize(width=win_width, height=win_height)  # Set window minimum size.
        self.eval("tk::PlaceWindow . center")
        self.mainloop()

    def menuGroup(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Compiler', menu=filemenu)

        filemenu.add_command(label='Settings', command=lambda: self.processUI('config'))
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=lambda: self.processUI('quit'))

        editmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Help', menu=editmenu)

        editmenu.add_command(label='About')  # TODO: Add about dialog
        editmenu.add_separator()
        editmenu.add_command(label='QuakePy Compiler')  # TODO: Add QuakePy Compiler help.
        editmenu.add_command(label='Quake Console Commands')  # TODO: Add Quake console command help.

    def mapGroup(self, parent):
        frame = tk.Frame(parent)  # Container for the map widgets section.
        frame.columnconfigure(index=1, weight=1)
        frame.pack(fill=X, pady=5)

        # Not needed, tk.Text widget currently setting width. #
        # map_str = self.settingStrVar['dev_map'].get()
        # entry_width = foo.widthForWidget(map_str)  # Calculate width for entry widget.

        mapLabel = tk.Label(frame, text="Dev Map:")
        mapLabel.grid(row=0, column=0, sticky=E)
        mapEntry = tk.Entry(frame, textvariable=self.settingStrVar['dev_map'])
        mapEntry.grid(row=0, column=1, sticky=EW)
        mapButton = tk.Button(frame, width=BTNWIDTH, text="...", command=lambda: self.processFileChange('dev_map'))
        mapButton.grid(row=0, column=2, sticky=E, padx=5)

    def compileGroup(self, parent):
        frame = tk.LabelFrame(parent, text="Compile Tools")  # Container for the compiler options. Options not implemented at this time.
        frame.columnconfigure(index=1, weight=1)
        frame.pack(fill=X)

        binLabel = tk.Label(frame, text="Tool Bin Path:")
        binLabel.grid(row=0, column=0, sticky=E, pady=5)
        binPathLabel = tk.Label(frame, textvariable=self.settingStrVar['tool_bin'])
        binPathLabel.grid(row=0, column=1, columnspan=2, sticky=W, pady=5)

        qbspOption_label = tk.Label(frame, text="qbsp options:")
        qbspOption_label.grid(row=1, column=0, sticky=E)
        qbspOption_entry = tk.Entry(frame, textvariable=self.toolOptStrVar['qbsp_opt'])
        qbspOption_entry.grid(row=1, column=1, sticky=EW, pady=5)
        qbspOption_button = tk.Button(frame, width=BTNWIDTH, text="?", command= lambda: self.toolHelpDialog('qbsp'))
        qbspOption_button.grid(row=1, column=2, sticky=E, padx=5)

        visOption_label = tk.Label(frame, text="vis options:")
        visOption_label.grid(row=2, column=0, sticky=E)
        visOption_entry = tk.Entry(frame, textvariable=self.toolOptStrVar['vis_opt'])
        visOption_entry.grid(row=2, column=1, sticky=EW, pady=5)
        visOption_button = tk.Button(frame, width=BTNWIDTH, text="?", command= lambda: self.toolHelpDialog('vis'))
        visOption_button.grid(row=2, column=2, sticky=E, padx=5)

        lightOption_label = tk.Label(frame, text="light options:")
        lightOption_label.grid(row=3, column=0, sticky=E)
        lightOption_entry = tk.Entry(frame, textvariable=self.toolOptStrVar['light_opt'])
        lightOption_entry.grid(row=3, column=1, sticky=EW, pady=5)
        lightOption_button = tk.Button(frame, width=BTNWIDTH, text="?", command=lambda: self.toolHelpDialog('light'))
        lightOption_button.grid(row=3, column=2, sticky=E, padx=5)

    def resultGroup(self, parent):
        frame = tk.LabelFrame(parent, text=" Tool Results ")  # Container for result widget, tk.Text & scrollbars.
        frame.rowconfigure(index=0, weight=1)
        frame.columnconfigure(index=0, weight=1)
        frame.pack(fill=X, pady=5, padx=5)

        scby = tk.Scrollbar(frame, orient=VERTICAL)
        scby.grid(row=0, column=1, sticky=NS)

        scbx = tk.Scrollbar(frame, orient=HORIZONTAL)
        scbx.grid(row=1, column=0, sticky=EW)

        resultText = tk.Text(frame, wrap=NONE, state=DISABLED, yscrollcommand=scby.set, xscrollcommand=scbx.set)
        resultText.grid(row=0, column=0, sticky=NSEW, padx=5)

        scby['command'] = resultText.yview
        scbx['command'] = resultText.xview

        return resultText

    def buttonGroup(self, parent):
        labels = "Compile", "Quake", "Quit"
        btn_width = max([foo.widthForWidget(l) for l in labels])  # Measure text to set the width of the button.

        frame = tk.Frame(parent)  # Container for the main UI processing buttons. Compile the map; Launch Quake with the compiled map or quit.
        frame.columnconfigure(index=0, weight=1)
        frame.pack(fill=X)

        compileButton = tk.Button(frame, width=btn_width, text=labels[0], command=lambda: self.processUI('compile'))
        compileButton.grid(row=0, column=0, sticky=E)

        quakeButton = tk.Button(frame, width=btn_width, text=labels[1], command=lambda: self.processUI('quake'))
        quakeButton.grid(row=0, column=1, sticky=E, pady=5, padx=5)

        quitButton = tk.Button(frame, width=btn_width, text=labels[2], command=lambda: self.processUI('quit'))
        quitButton.grid(row=0, column=2, sticky=E)

    def processUI(self, event):
        match event:
            case 'compile':
                dev_map = self.settingStrVar['dev_map'].get()
                devmap_name = os.path.split(dev_map)[-1]
                quake_bsp = os.path.splitext(devmap_name)[0]+".bsp"
                if dev_map:
                    os.chdir(os.path.split(dev_map)[0])
                    if os.path.isfile(dev_map):
                        launch_command = list()
                        launch_command.append(self.toolPath['qbsp'])
                        launch_command.append(dev_map)
                        foo.launch(self.resultText, launch_command)

                    if os.path.isfile(quake_bsp):
                        launch_command = list()
                        launch_command.append(self.toolPath['vis'])
                        launch_command.append(quake_bsp)
                        foo.launch(self.resultText, launch_command)

                        launch_command = list()
                        launch_command.append(self.toolPath['light'])
                        launch_command.append(quake_bsp)
                        foo.launch(self.resultText, launch_command)
                    id_folder = self.settingStrVar['id_folder'].get()
                    if id_folder:
                        try:
                            shutil.copy2(quake_bsp, os.path.join(id_folder, "maps"))
                        except Exception as err:
                            tmb.showerror("Error!", str(err))
                        else:
                            tmb.showinfo("Complete!", f"Quake Map {devmap_name} Copied to id1/maps")
            case 'quake':
                # OS Specifc Formatting to Execute Quake; *.exe for Windows *.app for Mac #
                if self.opsys == 'Windows':
                    launch_command = [self.settingStrVar['quake_engine'].get()]
                elif self.opsys == 'Darwin':  # Formatting to run the Quake app on Mac: prefix + app + suffix + command line arguments.
                    launch_command = MAC_PREFIX + [self.settingStrVar['quake_engine'].get()] + MAC_SUFFIX

                # Format Command Line Arguments, Replace <DEVFLDR> & <DEVMAP> Config Variables with the Path/File String #
                arg_list = self.settingStrVar['engine_arg'].get().split(' ')
                if '<DEVFLDR>' in arg_list or '<DEVMAP>' in arg_list:
                    for opt in arg_list:
                        if opt == '<DEVFLDR>':
                            launch_command.append(self.settingStrVar['dev_folder'].get())
                        elif opt == '<DEVMAP>':
                            dev_map = os.path.split(self.settingStrVar['dev_map'].get())[-1]
                            bsp = os.path.splitext(dev_map)[0] + ".bsp"  # Create *.bsp file name.
                            launch_command.append(bsp)
                        else:
                            launch_command.append(opt)
                else:
                    launch_command += arg_list  # Add user command line arguments if variables not used.

                foo.launch(self.resultText, launch_command) # Launch Quake!

            case 'config':
                self.configDialog()
            case 'quit':
                if self.settingStrVar['dev_map'].get() != self.app_config['dev_map']:
                    save = tmb.askquestion("Dev Map", "Save Map Selection?")
                    if save == 'yes':
                        self.saveConfig()
                self.destroy()

    ###   Help Dialog   ###
    def toolHelpDialog(self, tool):
        dlg = tk.Toplevel(self)

        dlgFrame = tk.Frame(dlg)
        dlgFrame.pack(expand=True, fill=BOTH)

        dlgText = self.dialogText(f" {tool} Help! ", dlgFrame)
        foo.launch(dlgText, self.toolPath[tool])

        dlg.mainloop()

    def dialogText(self, title, parent):
        frame = tk.LabelFrame(parent, text=title)
        frame.rowconfigure(index=0, weight=1)  # Allow contents to fill & expand.
        frame.columnconfigure(index=0, weight=1)  # Allow contents widget to fill & expand.
        frame.pack(fill=BOTH, expand=True, pady=5, padx=5)  # Allow frame to fill & expand.

        scby = tk.Scrollbar(frame, orient=VERTICAL)
        scby.grid(row=0, column=1, sticky=NS)

        scbx = tk.Scrollbar(frame, orient=HORIZONTAL)
        scbx.grid(row=1, column=0, sticky=EW)

        dlgText = tk.Text(frame, wrap=NONE, state=DISABLED, yscrollcommand=scby.set, xscrollcommand=scbx.set)
        dlgText.grid(row=0, column=0, sticky=NSEW, padx=5)

        scby['command'] = dlgText.yview
        scbx['command'] = dlgText.xview

        return dlgText

    ###   UI Config Dialog   ###
    def configDialog(self):
        widget_width = int(max([tkf.Font().measure(text=self.settingStrVar[s].get()) for s in SETTINGS])/8.5)

        dlg = tk.Toplevel(self)
        dlg.title("QuakePy Config")
        dlg.resizable(width=True, height=False)

        dlgFrame = tk.Frame(dlg)
        dlgFrame.pack(expand=True, fill=X, pady=5, padx=5)

        configFrame = tk.Frame(dlgFrame)
        configFrame.columnconfigure(index=1, weight=1)
        configFrame.pack(fill=X)

        devLabel = tk.Label(configFrame, text="Dev Folder:")
        devLabel.grid(row=0, column=0, sticky=E)
        devEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['dev_folder'])
        devEntry.grid(row=0, column=1, sticky=EW, pady=5, padx=5)
        devButton = tk.Button(configFrame, width=BTNWIDTH, text="...", command=lambda: self.processFolderChange('dev_folder'))
        devButton.grid(row=0, column=2, sticky=E)

        toolLabel = tk.Label(configFrame, text="Tool Bin:")
        toolLabel.grid(row=1, column=0, sticky=E)
        toolEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['tool_bin'])
        toolEntry.grid(row=1, column=1, sticky=EW, pady=5, padx=5)
        toolButton = tk.Button(configFrame, width=BTNWIDTH, text="...", command=lambda: self.processFolderChange('tool_bin'))
        toolButton.grid(row=1, column=2, sticky=E)

        engineLabel = tk.Label(configFrame, text="Quake Engine:")
        engineLabel.grid(row=2, column=0, sticky=E)
        engineEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['quake_engine'])
        engineEntry.grid(row=2, column=1, sticky=EW, pady=5, padx=5)
        engineButton = tk.Button(configFrame, width=BTNWIDTH, text="...", command=lambda: self.processFileChange('quake_engine'))
        engineButton.grid(row=2, column=2, sticky=E)

        argumentsLabel = tk.Label(configFrame, text="Arguments:")
        argumentsLabel.grid(row=3, column=0, sticky=E)
        argumentsEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['engine_arg'])
        argumentsEntry.grid(row=3, column=1, sticky=EW, pady=5, padx=5)
        argumentsButton = tk.Button(configFrame, width=BTNWIDTH, text="?", command=lambda: self.processFolderChange('engine_arg'))
        argumentsButton.grid(row=3, column=2, sticky=E)

        idLabel = tk.Label(configFrame, text="id Folder:")
        idLabel.grid(row=4, column=0, sticky=E)
        idEntry = tk.Entry(configFrame, width=widget_width, textvariable=self.settingStrVar['id_folder'])
        idEntry.grid(row=4, column=1, sticky=EW, pady=5, padx=5)
        idButton = tk.Button(configFrame, width=BTNWIDTH, text="...", command=lambda: self.processFolderChange('id_folder'))
        idButton.grid(row=4, column=2, sticky=E)

        buttonFrame = tk.Frame(dlgFrame)
        buttonFrame.columnconfigure(index=0, weight=1)
        buttonFrame.pack(fill=X)
        labels = "Save", "Cancel"
        btn_width = max([len(l) for l in labels])

        saveButton = tk.Button(buttonFrame, width=btn_width, text="Save", command=lambda: self.processConfigDialog(dlg, 'save'))
        saveButton.grid(row=0, column=0, sticky=E, pady=5, padx=5)

        cancelButton = tk.Button(buttonFrame, width=btn_width, text="Cancel", command=lambda: self.processConfigDialog(dlg, 'cancel'))
        cancelButton.grid(row=0, column=1, sticky=E, pady=5, padx=5)

        dlg.update_idletasks()
        win_width = dlg.winfo_width()
        win_height = dlg.winfo_height()
        dlg.minsize(width=win_width, height=win_height)
        dlg.mainloop()

    def processConfigDialog(self, win_obj, event):
        match event:
            case 'save':
                self.saveConfig()
            case 'cancel':
                win_obj.destroy()

    def saveConfig(self):
        for s in SETTINGS:
            self.app_config[s] = self.settingStrVar[s].get()
        for o in OPTIONS:
            self.app_config[o] = self.toolOptStrVar[o].get()
        foo.writeConfig(CONFIGFILE, self.app_config)

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


if __name__ == '__main__':
    if not os.path.exists(CONFIGFILE):
        tmb.showinfo("First Run!", "Enter Your Development Environment Information.")
        frd.firstRunDialog()
    Main()

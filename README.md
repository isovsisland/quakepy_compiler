# QuakePy Compiler

## A Python GUI interface for compiling Quake maps.

Written with Python 3.12 and tkinter.<br>

<pre>
Testing has been limited but includes:
- MacBook Air with M2 chip & Sonoma 14.6.1
- HP Envy Laptop & Windows 11 Home 23H2
</pre>

This script provides a graphical user interface inspired by necros compiling GUI. The inspiration came from wanting to use a similar GUI on my Mac machine. Like necros it utilizes ericw tools: qbsp, vis and light for the compiling functions. TrenchBroom has its own built in tool that you can configure to utilize the ericw compiling tools as well and TrenchBroom has a Mac version. So from a bare bones configuration Trenchbroom combined with ericw tools will cover it.

Additional features with the QuakePy Compiler include a help system and a results window. The help system provides the same help output as if you had typed "qbsp" in a terminal window but the output of all three tools is redirected to separate dialog windows. Compiling output for the tools are also redirected, but to the Results window in the main app.
QuakePy has a Quake launch button to run and view your map directly, without having to perform additional keystrokes to load the map into Quake, similar to necros and TrenchBroom.
Running an app in this manner on a Mac machine, for the coder, is a bit more tedious than Windows. Again, I have not done extensive testing but it seems to be working fine - at least on my machines. For those interested the command structure using this scenario as ana example: open -a /QuakeDev/YourQuakeFolder/QuakeApp.app --args -basedir /QuakeDev +map my_quake_map.map. The result is a dialog window created by the Mac OS to confirm the command and then you click start to proceed with launching the Quake app. A bit more than the requirements of windows.

For my Mac machine I use QuakeSpasm and for my Windows machine I use IronWail. vkQuake can also be used and is my preferred port when I'm actually playing a game because of the vulkan API. To me everything just looks better with vulkan. I am dissapointed by the anouncement that development of vkQuake has been stopped, but encouraged by what I see with IronWail. Hopefully a vulkan version is in its future.

Anyway, check out the excellent youtube video on TrenchBroom by dumptruck_ds for setting up your computer. The diagram below represents the directory structure on both my machines and is similar to the recomendation in the video. The folder names were copied from my Mac since my original intent was to write this script for Mac users. Its the same for my windows machine just with the windows versions.

<pre>
QuakeDev
|_TrenchBroom-macOS-v2024.1-Release
|_ericw-tools-v0.18.1-Darwin
| |_bin (qbsp, vis & light tools among others)
|
|_QuakeSpasm-0.96.3-osx-SDL2
|_wads
|_working
|_devmaps
|_id1
  |_maps (should already be in the id1 folder)
</pre>

<b>Setup:</b> The first time the script is run it will prompt you with a config dialog to fill in required folder and file path information. You can type in the path or use the button with the three dots to the right for the generic GUI selector.

<b>Dialog description from top to bottom:</b> Use the directory tree above as a reference.

- Dev Folder: (Your main development folder, QuakeDev in my case.)
- Tool Bin: (The "bin" folder in ericw-tools)
- Quake Engine: (The .app or .exe path & file in the QuakeSpasm folder or whatever port you are using)
- Arguments: (Command line arguments for your Quake engine. See note below.)
- id Folder: (Path to the id1 folder. The script will copy your newly compiled .bsp file to the id1/maps folder.

<em><b>Arguments</em> note:</b> I have set as a default the command line option "-basedir" which allows you to use an id1 folder that is external to your engine's folder, in this case QuakeSpasm. This is followed by an internal variable `<DEVFLDR>`. The script will automatically replace this variable with the actual Dev Folder path. Quake will find the id1 folder and launch normally. The second option "+map" and `<DEVMAP>` will specify your newly created map. Again the internal variable will be replaced by the script with your selection.

If you happen to experiment with the Arguments line and want to return to the original config, and forget the command structure; delete the config.json file and you will be prompted to create a new one. The Arguments detail will be populated automatically.

Click Save and you should be notified that something is missing or everything is ok and the main script will start. Then all you have to do is select your map, click the Compile button. If everything goes ok it will let you know tat it copied the compiled file (.bsp) to the id1/maps folder. Hitting the Quake button will launch Quake with your new map.

Enjoy and have fun!


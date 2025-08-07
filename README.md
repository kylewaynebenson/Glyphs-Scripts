# Glyphs Scripts
Python scripts for use in Glyphs.app.

## About Scripts
| Folder           | Script Name                     | Description |
|------------------|---------------------------------|-------------|
| Anchors          | Mirror Anchors Across Masters     | Takes a selected anchor and places it in corresponding positions across all masters based on positioning relative to zones and sides. |
| Components       | Add Corner Component            | Adds a selected corner component to the selected node(s) with the option to apply on all compatible masters (if masters are compatible). If multiple nodes are selected, it first applies the "sharpen corner" function. |
| Components       | Add Or Replace Components         | Replaces selected path or component with a new component in Glyphs 3. Options for automatic alignment, applying on all masters, and searching through all available glyphs. |
| Components       | Mirror Components Across Masters| Mirrors the components of the active layer to all other masters, updating any discrepancies. |
| Components       | Reset All Components            | Resets the scale of all components in the selected glyph to 100% with options for all masters and automatic alignment. |
| Components        | Reverse Component Path Direction | Reverses the path direction of a selected component. |
| Guides           | Local Guidelines                | Adds guidelines accross font based on guides found in various guide.extension glyphs |
| Interpolation    | Make Node First                   | Created this script so that I could assign a keyboard shortcut to this right-click function |
| Interpolation    | Count on Curve Points           | This counts all on curve points for each master or layer of a selected glyph. Made to help figure out interpolation issues on complex drawings. |
| Metrics    | Average Width                   | Adds up and averages the width of all the masters/layers for a selected glyph. I made it to help me figure out a good starting point width for tabular figures. |
| Metrics          | Change Width Centered | Kind of like a multiplexer, but more boring. Uniformly changes width, but keeps character centered. |
| Metrics           | Find Metrics          | Find metrics with specific characteristics and open in tab |
| Metrics          | Set Spacing Groups | Set Spacing Groups to spacing.extension if .extension is added |
| Paths           | Create Cast Shadow              | This creates a shadow as if the letter is a 3d object. You should probably not run this on more than 50 characters, as the process takes a little time. |
| Paths           | Create Drop Shadow              | Specify the size and direction of your drop shadow, with option to keep the letter, or just leave the shadow (handy if you want to create a font file of just shadows). |
| Paths           | Create Sign Painter Drop Shadow | This functions like Create Drop Shadow does, only it tries to blob things out a little bit, like it was painted instead of digitally generated. Definitely finagle with the settings before you give up on it. It requires fine tuning. |
| Paths             | Delete All Paths | Deletes all paths in selected glyphs. |
| Paths           | Delete Largest Path             | Deletes the largest path in the selected glyph. |
| Paths           | Keep Largest Path               | Keeps only the largest path in the selected glyph, deleting the rest. |
| Paths           | Delete Smallest Path            | Deletes the smallest path in the selected glyph. |
| Paths         | Keep Largest Path | Deletes all paths in selected glyphs except for the largest path. |
| Paths           | Randomly Move Points            | Jumbles the points within a certain specified amount. Lets you choose to only have OCP get jumbled. This is really only useful for making ugly things on purpose. |
| Paths           | Simplify Shape                  | This script reduces nodes at a ratio of your choosing. Best when used on grungy, messy, thousand+ node vectors. |


# Usage

Go to Glyphs.app: `window` > `Plugin Manager` > `Scripts`, then search for Kyle Wayne Benson.

# Other installation
Put the scripts into the *Scripts* folder which appears when you choose *Open Scripts Folder* from the *Scripts* menu.

For some scripts, you will also need to install Tal Leming's *Vanilla*. Here's how.

In **Glyphs 2.0 or later**, go to *Glyphs > Preferences > Addons > Modules* and click the *Install Modules* button. You are done and can skip the rest of these installation instructions.

For **Glyphs 1.x**, open Terminal and copy and paste the following lines and hit return. You can copy all of them at once. Notes: the second line (`curl`) may take a while, the `sudo` line will prompt you for your password (type it and press Return, you will *not* see bullets):

    cd ~/Library/
    curl http://download.robofab.com/RoboFab_599_plusAllDependencies.zip > robofab.zip
    unzip -o robofab.zip -d Python_Installs
    rm robofab.zip
    cd Python_Installs/Vanilla/
    sudo python2.6 setup.py install


And you are done. The installation should be effective immediately, but in case it does not work right away, you may want to restart your Mac or log out and back in again.

While we're at it, we can also install Robofab, DialogKit, and FontTools. You do not need those for my scripts though:

    cd ../Robofab/
    sudo python2.6 setup.py install
    cd ../DialogKit/
    sudo python2.6 install.py
    cd ../FontTools/
    sudo python2.6 setup.py install


## Credits
All my code borrows heavily from existing [mekkablue](https://github.com/mekkablue/), and definitely 100% couldn't exist without his prolific amounts of open source code. Praise be to him.

# License

Copyright 2017 Kyle Wayne Benson (@kylewaynebenson)
Some code samples by Rainer Erich Scheichelbauer (@mekkablue), Georg Seifert (@schriftgestalt) and Tal Leming (@typesupply).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use the software provided here except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.

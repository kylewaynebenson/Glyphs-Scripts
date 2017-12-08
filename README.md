# Glyphs Scripts
Python scripts I've created for use in Glyphs.app. I can give no promise that any of these work nor that they won't completely destroy your project so please use them with a good backup on your project.

## About Each Script
### Change Width Centered
This is kind of like a multiplexer, only more boring. You plug in a width, and it can adjust the RSB and LSB of all masters of a selected character to get it to that width. I created this script because Glyphs default behavior is to just add the space to the RSB. But with tabular figures, CJK full width latin characters, or a multiplexed font you'll want to keep the spacing pretty similar to how it previously was.
### Average Width
Adds up and averages the width of all the masters/layers for a selected glyph. I made it to help me figure out a good starting point width for tabular figures.
### Create Drop Shadow
There are tools like this available through the Glyphs Plugin Manager. The main difference here is that mine is probably more shitty, and mine has the option to keep the letter, or just leave the shadow—which is handy if you want to create a font file of just shadows.
### Create Cast Shadow
This creates a shadow as if the letter is a 3d object. You should probably not run this on more than 50 characters, as the process takes a little time.
### Create Sign Painter Drop Shadow
This functions like Create Drop Shadow does, only it tries to blob things out a little bit, like it was painted instead of digitally generated. Definitely finagle with the settings before you give up on it. It requires fine tuning in order to perform.
### Simplify Shape
This script reduces nodes at a ratio of your choosing. Best when used on grungy, messy, thousand+ node vectors.
### Randomly Move Points
Jumbles the points within a certain specified amount. Lets you choose to only have OCP get jumbled. This is really only useful for making ugly things on purpose.
### Delete Largest Path/Keep Largest Path/Delete Smallest Path
I made these to delete some of the accidental shapes that were left after running Create Cast Shadow or other path manipulating scripts.
### Count on Curve Points
This counts all on curve points for each master or layer of a selected glyph. Made to help figure out interpolation issues on complex drawings.

# Installation

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

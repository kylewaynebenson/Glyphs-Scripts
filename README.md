# Glyphs Scripts
Python scripts I've created for use in Glyphs.app. I can give no promise that any of these work nor that they won't completely destroy your project so please use them with a good backup on your project.

## Installation

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

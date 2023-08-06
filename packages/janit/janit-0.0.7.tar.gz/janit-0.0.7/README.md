Janit
=====
Janit is a Multiplexer and a “command-line environment”. 
It gives you:
------------
  * Access to a menu for running desktop applications
  * As many terminals as you want
  * Simple Python methods that yield bash commands
  
Want it?
--------

From source 
-----------
* git clone https://hackersgame@bitbucket.org/hackersgame/janit.git
* cd janit
* sudo python3 setup.py install

By hand
-------
* git clone https://hackersgame@bitbucket.org/hackersgame/janit.git
* Install pyte, readchar, curses
  * pip install pyte # Or install my patched version (better support for w3m) git clone https://github.com/ruapotato/pyte
* Link to bin
  * sudo ln -s /path/to/janit.py /usr/bin/janit


license
-------
GPL3
By David Hamner

Janit Man:
----------
  * manual command
    * run 'manual' for additional help
    
  * Navigation:
    * ctrl + left/right to open/change terminal window (That’s the multiplexing part) 
    * ctrl + up/down with switch between terminal window and menu system
    * The <enter key> from the menu without a command will switch to the Terminal too
 
  * Menu system:
    * Run an application by entering:  name <tab to auto-complete>
    * TODO: To see the menu of installed programs hit <tab> without text
       * sub-menus can be seen by entering the sub-menu name 
       * (the sub-menu names will be ignore when the command is run) 

  * Target system:
    * From the menu you can enter a path to a file (~ and ./ will be turned into an absolute path) 
       * <tab> at this point will show the applications that can run the file type 
       * Running a command will now pass the target into the program as an argument 
    * Run “done” to unset the target 
    * Run “next” to try to toggle to the next alike file.
       * Example: a target of: “/home/Data/my Favorite Show/S01/e01.mp4” would become ../e02.mp4
    * Run “back” to try to toggle to the previous alike file

  * [Removed] Splitting terminals [Removed]:
    * You can split any open terminal in janit
      * <TermNumber> is shown in top left most corner
      * <TermNumber> separated by spaces, will split horizontally
        * Example: 0 1
      * <TermNumber> separated by slash, will split vertically
        * Example: 0/1
      * Example: 
        * Open 4 windows with Ctrl + Right
        * Run: 1 2/3 4
        * You should see the terminal split 4 ways
        * Run: 1
        * You should only see one terminal again


Todo:
-----
  * History clear/loading when switching terminal
  * redo <tab> menu 
  * key up and down (in menu and as history)
  * show apps run more often first (for auto comp) 
  * .desktop with multiple entrys will not load right

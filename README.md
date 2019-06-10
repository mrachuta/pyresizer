## Project name
pyresize - a python tool, that allows to resize a large number of images in one click.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Using](#using)
* [Thanks](#thanks)

## General info
Idea for tool was born due to problems in departament that I working for.
None of PC has permissions to install external software, so each of users 
has problems with fast & simple resizing of photos. Some of people was using 
old IrfanView versions, another using pre-installed Microsoft PhotoEditor. 
Both of them are slow and for some users not intuitive. Additionally, photos 
was resizing to various dimensions.

App was aimed to:

a) be fast,  
b) be light,  
c) be compatible with Windows7/8/10,  
d) require no administration privileges to install and running,  
e) require as less user integration as possible,  
f) automate process as much as possible.  

Only goal b) was not fulfilled (what in case of executables made 
from Python scripts, is a normal thing)

## Technologies
Python 3.
File was compilled to executable using pyInstaller.

Code was tested on following platforms:

a) Windows 8.1 (PL-PL) (x64) with Python 3.7.1  
b) Windows 8.1 (EN-US) (x64) with Python 3.6.4  
c) Windows 7 (PL-PL) (x64) with Python 3.7.1  

Used libraries:
* altgraph==0.16.1
* future==0.17.1
* macholib==1.11
* pefile==2019.4.18
* Pillow==6.0.0
* PyInstaller==3.4
* pywin32-ctypes==0.2.0

## Setup

1. Clone git repo to localhost,
2. Install required packages (optional, if you want to use pyresizer as Python script)
  
## Using

- executable:  

  to run, perform:
  ```
  pyresizer
  ```
- script:  

  to run, perform:
  ```
  python pyresizer.py
  ```

ATTENTION: tool automatically convert all image-files in folder, where you started it.
Don't worry, originals are always available in *bak* folder, automatically created 
in the same localization where you ran the tool.

Available options:

-h - see help,  
-i - install as context-menu tool (available only for executable verison),  
-u - remove from context-menu (available only for executable version).  

## Thanks

For me :)
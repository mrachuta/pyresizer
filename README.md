## Project name
pyresize - a python tool, that allows to resize a large number of images in one click.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
* [Thanks](#thanks)

## General info
Idea for tool was born due to problems in departament that I working for.
My user account has no permissions to install external software, so I was 
unable to install any external resizing tools. Some people were using 
old IrfanView versions, other were using pre-installed Microsoft PhotoEditor. 
Both of them are slow and for some users not intuitive.

App is aimed to:

a) be fast,  
b) be lightweight,  
c) be compatible with Windows7/8/10,  
d) require no administration privileges to install and run,  
e) require as less user integration as possible,  
f) automate process as much as possible.  

Only goal b) was not fulfilled (because of size of executable)

## Technologies
* Python 3.

File was compilled to executable using pyInstaller.

Code was tested on following platforms:

* Windows 8.1 (PL-PL) (x64) with Python 3.7.1  
* Windows 8.1 (EN-US) (x64) with Python 3.6.4  
* Windows 7 (PL-PL) (x64) with Python 3.7.1  

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
2. OPTIONAL: Install required packages (if you want to use pyresizer as Python script)
  
## Usage

Open console and change directory to cloned repository and run:

- for executable:  
  ```
  pyresizer
  ```
- for script:  
  ```
  python3 pyresizer.py
  ```

WARNING: tool is automatically converting all images in folder where you started it.
Don't worry, original files are always available in *bak* folder, automatically created 
in current working directory.

Available options:
```
-h - see help,  
-i - install as context-menu tool (available only for executable verison),  
-u - remove from context-menu (available only for executable version).  
```
## Thanks

For me :)

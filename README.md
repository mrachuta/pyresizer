## Project name
pyresizer - a python tool, that allows to resize a large number of images in one shot.

## Table of contents
- [Project name](#project-name)
- [Table of contents](#table-of-contents)
- [General info](#general-info)
- [Technologies](#technologies)
- [Setup](#setup)
  - [From bundle](#from-bundle)
  - [From sources](#from-sources)
  - [Removal](#removal)
- [Usage](#usage)


## General info
The idea for the tool was born due to problems in the department that I worked for. None of PCs has permissions to install external software, so each of users 
has problems with quick & easy resizing of photos. Some of people were using old IrfanView versions, another used pre-installed Microsoft PhotoEditor.  Both of them are slow and not intuitive for some users. Additionally, photos were resized to different dimensions. It was a good time to introduce some standardisation.

App is aimed to:
  - be fast,  
  - be lightweight (if Python can be so),
  - be compatible with Windows 10/11 and Linux,
  - require no administration privileges to install, run and uninstall,
  - require as less user interaction as possible 

## Technologies
Just Python.

Code was tested on following platforms:
  - Windows 10 with Python 3.9
  - Windows 11 with Python 3.13
  - Linux with Python 3.13
  - Linux with Python 3.9

Libraries required to run are available in *requirements.txt* file.

## Setup

### From bundle

1. Download latest release from Github Releases tab
2. Install:
     - Windows
       ```
       pyresizer.exe -i
       ```
       This command installs pyresizer in you App Data directory and adds an entry to the context menu to use it in any directory you want in simple way.
     - Linux
       ```
       pyresizer -i
       ```
       This command installs pyresizer in *$HOME/.local/bin* and modifies *.bashrc* by adding path to $PATH variable if path it does not already exists.

### From sources

1. Clone git repo to localhost
2. Create virtualenv (example for virtualenvwrapper)
    ```
    cd pyresizer && mkvirtualenv pyresizer
    pip install -r requirements.txt
    ```
3. Build package (executable will be available in *dist* folder)
    ```
    pyinstaller -F pyresizer.py
    ```
4. See setup from bundle, point no. 2

### Removal

1. Perform following command to remove tool:
     - Windows
       ```
       pyresizer.exe -u
       ```
       This command removes pyresizer from your App Data directory and the entry from the context menu.
     - Linux
       ```
       pyresizer -u
       ```
       This command removes pyresizer from *$HOME/.local/bin* and remove $PATH update from *.bashrc* (only, if it has been added previously).

## Usage

- Run
  ```
  pyresizer
  ```
- Run with custom image size
  ```
  pyresizer -x 2400 -y 3200
  ```
- Help
  ```
  pyresizer -h
  ```

ATTENTION: the tool will automatically convert all the images in the folder, where you run it.
Don't worry, the original file are always available in *bak* folder in the same location.

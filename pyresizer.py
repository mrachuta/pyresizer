# -*- Coding: UTF-8 -*-

import winreg
import argparse
from sys import argv
from shutil import copy2, rmtree
from os import listdir, path, mkdir
from PIL.Image import open, ANTIALIAS


class Resizer:

    """Main functionality of tool"""

    def __init__(self):
        # Both sizes could be changed according to requirements
        self.img_width = 1200
        self.img_height = 1600
        self.img_dims = (self.img_width, self.img_height)
        self.img_formats = ['.bmp', '.gif', '.jpg', '.jpeg', '.png']
        self.bak_folder = 'bak'

    # Keep image list always up-to-date
    @property
    def get_imgs(self):
        return [
            str(i.lower())
            for i in listdir()
            if path.isfile(i) and any(x in i for x in self.img_formats)
        ]

    def make_backups(self):
        print('Creating original images backup...')
        try:
            if not path.exists(self.bak_folder):
                mkdir(self.bak_folder)
            for i in self.get_imgs:
                copy2(i, path.join(self.bak_folder, i))
            print('Backup created.')
        except IOError:
            print('Error: unable to create backup.')
            dec = input('Do you want to proceed to next step? [y/n]: ')
            if dec.lower() == 'y':
                return True
            else:
                return False

    def resize_files(self):
        imgs_quantity = len(self.get_imgs)
        if imgs_quantity:
            print(f'{imgs_quantity} files will be processed')
        else:
            print('Error: no images to processing found.')
            return False
        try:
            self.make_backups()
            for index, i in enumerate(self.get_imgs):
                print(f'Resizing {i} ({index+1} of {imgs_quantity})')
                im = open(i)
                im.thumbnail(self.img_dims, ANTIALIAS)
                im.save(i)
                print(f'Resizing {i} finished.')
            print('Processing finished.')
        except IOError:
            print('Error: some files was not processed.')
            return False


class InstallerUninstaller:

    """Installation or uninstallation of tool"""

    def __init__(self):
        
        self.app_name = 'pyresizer'

        """
        Installation target_path and registry root-path path can be changed, 
        but this configuration allows user to install tool without administrator 
        privileges.
        """

        self.user_home = path.join(path.expanduser('~'), 'AppData', 'Local')
        self.curr_file_path = path.join(
            path.dirname(path.abspath(__file__)), 
            [argv[0] if '.exe' in argv[0] else argv[0]+'.exe'][0]
        )
        self.target_path = path.join(self.user_home, self.app_name, self.app_name+'.exe')
        self.reg_path = r'Software\Classes\Directory\Background\shell\pyresizer'

    def modify_context_menu(self):

        print('Adding registry keys...')
        try:
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.reg_path)
            winreg.SetValue(reg_key, None, winreg.REG_SZ, 'Use pyresizer here')
            # Registry key for icon
            winreg.SetValueEx(reg_key, 'Icon', 0, winreg.REG_SZ, self.target_path)
            # Registry key responsible for command, which will be executed
            reg_key_command = winreg.CreateKey(reg_key, 'command')
            winreg.SetValue(reg_key_command, None, winreg.REG_SZ, self.target_path)
            winreg.CloseKey(reg_key_command)
            winreg.CloseKey(reg_key)
            print('Registry keys added successfully.')
        except OSError:
            print('Error: unable to add registry keys.')
            return False

    def copy_file(self):

        print('Copying executable file...')
        target_folder = path.join(self.user_home, self.app_name)
        try:
            if not path.exists(target_folder):
                mkdir(path.join(self.user_home, self.app_name))

            copy2(self.curr_file_path, self.target_path)
            print('Executable file copied successfully.')
            self.modify_context_menu()
        except IOError:
            print('Error: executable file not copied')
            return False

    def remove_file(self):

        print('Removing executable file...')
        if path.exists(self.target_path):
            rmtree(path.dirname(self.target_path), ignore_errors=False, onerror=None)
            print('Executable file removed.')
        else:
            print('Executable file not found, maybe app is not installed?')

    def revert_context_menu(self):

        print('Removing registry keys...')
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.reg_path + r'\command')
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.reg_path)
            print('Registry keys removed.')
        except OSError:
            print('Registry keys not found, maybe app is not installed?')


def core():
    print(
        """\
        ┌─┐┬ ┬┬─┐┌─┐┌─┐┬┌─┐┌─┐┬─┐
        ├─┘└┬┘├┬┘├┤ └─┐│┌─┘├┤ ├┬┘
        ┴   ┴ ┴└─└─┘└─┘┴└─┘└─┘┴└─
        (c) 2019. 
        \nType -h or --help to see more information.
        """
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--install', help='Install to the context menu', action='store_true'
    )
    parser.add_argument(
        '-u', '--uninstall', help='Remove from the context menu', action='store_true'
    )
    args = parser.parse_args()
    if args.install:
        print('Installing pyresizer...')
        installer = InstallerUninstaller()
        # Due to nested function, installation of script is not possible
        installer.copy_file()
    elif args.uninstall:
        print('Uninstalling pyresizer...')
        uninstaller = InstallerUninstaller()
        uninstaller.remove_file()
        uninstaller.revert_context_menu()
    else:
        resizer = Resizer()
        # Nested functions again, to prevent inform user about successful conversion
        if resizer.resize_files():
            print('Resizing finished.')
        input('Press enter to exit...')
        raise SystemExit


if __name__ == '__main__':
    core()

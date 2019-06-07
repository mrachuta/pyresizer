# -*- Coding: UTF-8 -*-

import winreg
import argparse
from sys import argv
from shutil import copy2, rmtree
from os import listdir, path, mkdir
from PIL.Image import open, ANTIALIAS


class Resizer:
    def __init__(self):
        self.img_width = 1200
        self.img_height = 1600
        self.img_dims = (self.img_width, self.img_height)
        self.img_formats = [".bmp", ".gif", ".jpg", ".jpeg", ".png"]
        self.bak_folder = "bak"

    @property
    def get_imgs(self):
        return [
            str(i.lower())
            for i in listdir()
            if path.isfile(i) and any(x in i for x in self.img_formats)
        ]

    def make_backups(self):
        if not path.exists(self.bak_folder):
            mkdir(self.bak_folder)
        for i in self.get_imgs:
            copy2(i, path.join(self.bak_folder, i))

    def resize_files(self):
        for i in self.get_imgs:
            im = open(i)
            im.thumbnail(self.img_dims, ANTIALIAS)
            im.save(i)


class InstallerUninstaller:
    def __init__(self):

        self.user_home = path.join(path.expanduser("~"), "AppData", "Local")
        self.curr_file_path = path.join(path.dirname(path.abspath(__file__)), argv[0])
        self.target_path = path.join(self.user_home, "pyresizer", "pyresizer.exe")
        self.reg_path = r"Software\Classes\Directory\Background\shell\pyresizer"

    def copy_file(self):

        print("Copying executable file...")
        target_folder = path.join(self.user_home, "pyresizer")

        if not path.exists(target_folder):
            mkdir(path.join(self.user_home, "pyresizer"))

        copy2(self.curr_file_path, self.target_path)
        print("Executable file copied successfully.")

    def modify_context_menu(self):

        print("Adding registry keys...")
        try:
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.reg_path)
            winreg.SetValue(reg_key, None, winreg.REG_SZ, "Use pyresizer here")
            winreg.SetValueEx(reg_key, "Icon", 0, winreg.REG_SZ, self.target_path)
            reg_key_command = winreg.CreateKey(reg_key, "command")
            winreg.SetValue(reg_key_command, None, winreg.REG_SZ, self.target_path)
            winreg.CloseKey(reg_key_command)
            winreg.CloseKey(reg_key)
            print("Registry keys added successfully.")
        except OSError:
            print("Unable to add registry keys.")

    def remove_file(self):

        print("Removing executable file...")
        if path.exists(self.target_path):
            rmtree(path.dirname(self.target_path), ignore_errors=False, onerror=None)
            print("Executable file removed.")
        else:
            print("Executable file not found, maybe app is not installed?")

    def revert_context_menu(self):

        print("Removing registry keys...")
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.reg_path + r"\command")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.reg_path)
            print("Registry keys removed.")
        except OSError:
            print("Registry keys not found, maybe app is not installed?")


def core():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--install", help="Install to the context menu", action="store_true"
    )
    parser.add_argument(
        "-u", "--uninstall", help="Remove from the context menu", action="store_true"
    )
    args = parser.parse_args()
    if args.install:
        print("Installing pyresizer...")
        installer = InstallerUninstaller()
        installer.copy_file()
        installer.modify_context_menu()
        print("Installation finished")
    elif args.uninstall:
        print("Uninstalling pyresizer...")
        uninstaller = InstallerUninstaller()
        uninstaller.remove_file()
        uninstaller.revert_context_menu()
        print("Uninstallation finished")
    else:
        inst = Resizer()
        inst.make_backups()
        inst.resize_files()


if __name__ == "__main__":
    core()

#!/usr/bin/env python3

import argparse
import platform
import sys
from os import listdir as os_listdir
from os import mkdir as os_mkdir
from os import path as os_path
from os import remove as os_remove
from re import MULTILINE as re_MULTILINE
from re import compile as re_compile
from shutil import copy2 as shutil_copy2
from shutil import rmtree as shutil_rmtree

from PIL.Image import Resampling as pil_Resampling
from PIL.Image import open as pil_open

if platform.system() == "Windows":
    import winreg


class Resizer:
    """Main functionality of tool"""

    def __init__(self, new_width):
        # Both sizes could be changed according to requirements
        self.new_width = new_width
        self.img_formats = [".bmp", ".gif", ".jpg", ".jpeg", ".png"]
        self.bak_folder = "bak"

    # Keep image list always up-to-date
    @property
    def get_imgs(self):
        return [
            str(i)
            for i in os_listdir()
            if os_path.isfile(i) and any(x in i.lower() for x in self.img_formats)
        ]

    def make_backups(self):

        print("Backing up original images...")
        try:
            if not os_path.exists(self.bak_folder):
                os_mkdir(self.bak_folder)
            for i in self.get_imgs:
                shutil_copy2(i, os_path.join(self.bak_folder, i))
            print("Backup created.")
            return True
        except IOError:
            print("Error: unable to create backup!")
            dec = input("Do you want to proceed to next step? [y/n]: ")
            return bool(dec.lower() == "y")

    def resize_files(self):

        imgs_quantity = len(self.get_imgs)
        if imgs_quantity > 0:
            print(f"{imgs_quantity} files will be processed")
        else:
            print("No images to be processed.")
            return True
        try:
            self.make_backups()
            for index, i in enumerate(self.get_imgs):
                print(f"Resizing {i} ({index+1} of {imgs_quantity})...")
                im = pil_open(i)
                im_width, im_height = im.size
                new_height = self.new_width * im_height / im_width
                img_dims = (self.new_width, new_height)
                im.thumbnail(img_dims, pil_Resampling.LANCZOS)
                im.save(i)
                print(f"Resizing {i} finished.")
            print("Processing finished.")
            return True
        except IOError as exc:
            raise IOError("Error: some files were not processed!") from exc


class InstallerUninstaller:
    """Installation or uninstallation of tool"""

    textEncoding = "utf-8"

    def __init__(self, app_name):

        if not getattr(sys, "frozen", False):
            raise SystemError(
                "Error: cannot install Python file because of dependecies."
            )

        self.home_dir = os_path.expanduser("~")

        self.app_executable = os_path.basename(sys.argv[0])
        self.curr_file_path = os_path.join(
            os_path.dirname(sys.executable), self.app_executable
        )

        if platform.system() == "Windows":
            # Subdir
            self.install_path = os_path.join(
                self.home_dir, "AppData", "Local", app_name
            )
            self.reg_path = (
                f"Software\\Classes\\Directory\\Background\\shell\\{app_name}"
            )
        elif platform.system() == "Linux":
            # No subdir
            self.install_path = os_path.join(self.home_dir, ".local", "bin")
            self.default_bash_file = f"{self.home_dir}/.bashrc"
        else:
            raise SystemError(
                "Error: cannot continue installation. Unsupported platform."
            )

        self.full_path = os_path.join(self.install_path, self.app_executable)

    def _remove_from_windows_context_menu(self):

        if platform.system() == "Windows":
            try:
                print("Removing application from context menu registry keys...")
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"{self.reg_path}\\command")
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.reg_path)
                print("Registry keys removed.")
                return True
            except OSError as exc:
                raise OSError("Error: unable to remove registry keys!") from exc
        else:
            raise SystemError(
                "Error: cannot continue installation. Unsupported platform."
            )

    def _add_to_windows_context_menu(self):

        if platform.system() == "Windows":
            try:
                print("Adding application to context menu registry keys...")
                reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.reg_path)
                winreg.SetValue(reg_key, None, winreg.REG_SZ, "Use pyresizer here")
                # Registry key for icon
                winreg.SetValueEx(
                    reg_key,
                    "Icon",
                    0,
                    winreg.REG_SZ,
                    f"{self.install_path}\\{self.app_executable}",
                )
                # Registry key responsible for command, which will be executed
                reg_key_command = winreg.CreateKey(reg_key, "command")
                winreg.SetValue(
                    reg_key_command,
                    None,
                    winreg.REG_SZ,
                    f"{self.install_path}\\{self.app_executable}",
                )
                winreg.CloseKey(reg_key_command)
                winreg.CloseKey(reg_key)
                print("Registry keys added successfully.")
                return True
            except OSError as exc:
                raise OSError("Error: unable to add registry keys!") from exc
        else:
            raise SystemError(
                "Error: cannot continue installation. Unsupported platform."
            )

    def _add_to_linux_path(self):

        print("Adding application to $PATH...")
        bash_files_and_dirs = [
            f"{self.home_dir}/.bashrc",
            f"{self.home_dir}/.profile",
            f"{self.home_dir}/.bash_profile",
            f"{self.home_dir}/.bash.login",
            f"{self.home_dir}/.bash_aliases",
            "/etc/bash.bashrc",
            "/etc/profile",
            "/etc/profile.d",
            "/etc/environment",
        ]

        existing_files = []
        for bash_path in bash_files_and_dirs:
            try:
                if os_path.exists(bash_path):
                    if os_path.isdir(bash_path):
                        files_in_dir = [
                            os_path.join(bash_path, f) for f in os_listdir(bash_path)
                        ]
                        existing_files.extend(files_in_dir)
                    else:
                        existing_files.append(bash_path)
            except Exception as exc:
                raise SystemError(
                    f"Error: error during reading object: {bash_path}"
                ) from exc

        for bash_file in existing_files:
            try:
                print(
                    f"Checking file {bash_file} against presence of $HOME/.local/bin in $PATH..."
                )
                with open(bash_file, "r", encoding=self.textEncoding) as f:
                    for line in f:
                        if re_compile(r"^PATH=.*\$HOME\/\.local\/bin").search(line):
                            print(
                                f"$HOME/.local/bin found in $PATH in file {bash_file}. "
                                + "Changes in $PATH not needed."
                            )
                            return True
            except Exception as exc:
                raise SystemError(
                    f"Error: error during reading object {bash_file}"
                ) from exc

        print(
            "$HOME/.local/bin not found in $PATH in any of files. "
            + f"Adding changes to {self.default_bash_file}"
        )
        try:
            with open(
                f"{self.default_bash_file}", "a", encoding=self.textEncoding
            ) as f:
                f.write(
                    "# Update added by pyresizer\n"
                    + 'PATH="$HOME/.local/bin:$PATH"\nexport $PATH\n'
                    + "# End of pyresizer update\n\n"
                )
            print("$PATH modified. Reload your bash please.")
            return True
        except Exception as exc:
            raise SystemError(
                f"Error: error during writing object {self.default_bash_file}"
            ) from exc

    def _remove_from_linux_path(self):

        try:
            print("Removing application from $PATH...")
            with open(
                f"{self.default_bash_file}", "r", encoding=self.textEncoding
            ) as f:
                file_content = f.read()
            # Get content and replace
            update_pattern = re_compile(
                r"# Update added by pyresizer\n"
                + r'PATH="\$HOME/\.local/bin:\$PATH"\nexport \$PATH\n'
                + r"# End of pyresizer update\n\n",
                re_MULTILINE,
            )
            if not update_pattern.search(file_content):
                print(
                    "$PATH not modified by application, pattern not found. Skipping..."
                )
                return True

            new_content = update_pattern.sub("", file_content)
            with open(
                f"{self.default_bash_file}", "w", encoding=self.textEncoding
            ) as f:
                f.write(new_content)
            print("$PATH modified. Reload your bash please.")
            return True
        except Exception as exc:
            raise SystemError(
                f"Error: error during reading or writing object {self.default_bash_file}"
            ) from exc

    def copy_file(self):

        if platform.system() not in ["Windows", "Linux"]:
            raise SystemError(
                "Error: cannot continue installation. Unsupported platform."
            )

        print("Copying executable file...")
        try:
            if not os_path.exists(self.install_path):
                os_mkdir(self.install_path)

            shutil_copy2(self.curr_file_path, self.full_path)
            print(f"Executable file copied successfully to {self.full_path}.")
        except IOError as exc:
            raise IOError("Error: executable file not copied!") from exc

        if platform.system() == "Windows":
            self._add_to_windows_context_menu()

        if platform.system() == "Linux":
            self._add_to_linux_path()

        print("Installation completed!")
        return True

    def remove_file(self):

        if platform.system() not in ["Windows", "Linux"]:
            raise SystemError(
                "Error: cannot continue uninstallation. Unsupported platform."
            )

        if platform.system() == "Windows":
            try:
                print("Removing subdirectory together with executable file...")
                shutil_rmtree(
                    # Trailing delimiter is extremely important (or direct path to file)
                    # to ensure deletion of only target dir with it's content.
                    os_path.dirname(self.full_path),
                    ignore_errors=False,
                    onerror=None,
                )
                print(
                    f"Subdirectory together with executable file removed {self.full_path}."
                )
            except OSError as exc:
                raise OSError(
                    "Error: subdirectory together with executable file not removed!"
                ) from exc
            self._remove_from_windows_context_menu()

        if platform.system() == "Linux":
            print("Removing executable file...")
            try:
                os_remove(self.full_path)
                print(f"Executable file removed from {self.full_path}.")
            except OSError as exc:
                raise OSError("Error: executable file not removed!") from exc
            self._remove_from_linux_path()

        print("Uninstallation completed!")
        return True


def main():

    sys.stdout.reconfigure(encoding=InstallerUninstaller.textEncoding)
    script = os_path.basename(sys.argv[0])
    app_name = "pyresizer"
    desc = f"{app_name} 2.0.0. Script to quickly resize images."
    parser = argparse.ArgumentParser(prog=script, description=desc)

    print(
        """\n
        ┌─┐┬ ┬┬─┐┌─┐┌─┐┬┌─┐┌─┐┬─┐
        ├─┘└┬┘├┬┘├┤ └─┐│┌─┘├┤ ├┬┘
        ┴   ┴ ┴└─└─┘└─┘┴└─┘└─┘┴└─
        \nType -h or --help to see more information.
        """
    )

    parser.add_argument(
        "-i",
        "--install",
        help="Install to the context menu",
        action="store_true",
    )
    parser.add_argument(
        "-u",
        "--uninstall",
        help="Remove from the context menu",
        action="store_true",
    )
    parser.add_argument(
        "-x",
        "--width",
        help="New image width (height will be adjusted automatically to keep aspect ration)",
        type=int,
        default=1200,
    )
    args = parser.parse_args()
    if args.install:
        print("Installing pyresizer...")
        installer = InstallerUninstaller(app_name)
        installer.copy_file()
    elif args.uninstall:
        print("Uninstalling pyresizer...")
        uninstaller = InstallerUninstaller(app_name)
        uninstaller.remove_file()
    else:
        resizer = Resizer(args.width)
        resizer.resize_files()
        input("Press ENTER key to exit...")


if __name__ == "__main__":
    main()

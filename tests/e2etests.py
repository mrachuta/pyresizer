import os
import platform
import re
import shutil
import subprocess
import time
import unittest

from PIL import Image as PILImage


class TestE2E(unittest.TestCase):

    CWD = os.path.dirname(os.path.abspath(__file__))
    SCRIPT_PATH = os.path.join(CWD, "..", "dist")
    BLACK_FILENAME = "full-black-4k.png"
    RED_FILENAME = "full-red-4k.jpg"

    def setUp(self):

        self.subprocess_required_args = {
            "cwd": self.SCRIPT_PATH,
            "capture_output": True,
            "text": True,
            "shell": True,
            "encoding": "utf-8",
        }
        if platform.system() == "Windows":
            self.executable = "pyresizer.exe"
        elif platform.system() == "Linux":
            self.executable = "./pyresizer"
        else:
            raise SystemError("Error: cannot continue E2E tests. Unsupported platform.")
        # Copy resources required by tests
        files_to_copy = [
            os.path.join(self.CWD, "resources", f)
            for f in os.listdir(os.path.join(self.CWD, "resources"))
            if re.search(r".*\.(jpg|png)$", f)
        ]
        for f in files_to_copy:
            shutil.copy2(f, self.SCRIPT_PATH)

    def tearDown(self):
        files_to_remove = [
            os.path.join(self.SCRIPT_PATH, f)
            for f in os.listdir(self.SCRIPT_PATH)
            if re.search(r".*\.(jpg|png)$", f)
        ]
        # Ignore files with new size
        for f in files_to_remove:
            os.remove(f)
        # Remove bak folder and it's content
        shutil.rmtree(os.path.join(self.SCRIPT_PATH, "bak"), ignore_errors=True)

    def testHelp(self):
        result = subprocess.run(
            [self.executable + " --help"], **self.subprocess_required_args
        )
        self.assertIn("optional arguments:", result.stdout)

    def testDefaultResizing(self):
        subprocess.run([self.executable], **self.subprocess_required_args)
        with PILImage.open(
            os.path.join(self.SCRIPT_PATH, self.BLACK_FILENAME)
        ) as image_png:
            image_png_width, image_png_height = image_png.size
            self.assertEqual(image_png_width, 1200)
            self.assertEqual(image_png_height, 675)
        with PILImage.open(
            os.path.join(self.SCRIPT_PATH, self.RED_FILENAME)
        ) as image_jpg:
            image_jpg_width, image_jpg_height = image_jpg.size
            self.assertEqual(image_jpg_width, 1200)
            self.assertEqual(image_jpg_height, 675)

    def testCustomResizing(self):
        subprocess.run(
            [self.executable + " --width 2000"], **self.subprocess_required_args
        )
        with PILImage.open(
            os.path.join(self.SCRIPT_PATH, self.BLACK_FILENAME)
        ) as image_png:
            image_png_width, image_png_height = image_png.size
            self.assertEqual(image_png_width, 2000)
            self.assertEqual(image_png_height, 1125)
        with PILImage.open(
            os.path.join(self.SCRIPT_PATH, self.RED_FILENAME)
        ) as image_jpg:
            image_jpg_width, image_jpg_height = image_jpg.size
            self.assertEqual(image_jpg_width, 2000)
            self.assertEqual(image_jpg_height, 1125)

    def testBackupsCreated(self):
        subprocess.run([self.executable], **self.subprocess_required_args)
        with PILImage.open(
            os.path.join(self.SCRIPT_PATH, "bak", self.BLACK_FILENAME)
        ) as image_png:
            image_png_width, image_png_height = image_png.size
            self.assertEqual(image_png_width, 3840)
            self.assertEqual(image_png_height, 2160)
        with PILImage.open(
            os.path.join(self.SCRIPT_PATH, "bak", self.RED_FILENAME)
        ) as image_jpg:
            image_jpg_width, image_jpg_height = image_jpg.size
            self.assertEqual(image_jpg_width, 3840)
            self.assertEqual(image_jpg_height, 2160)

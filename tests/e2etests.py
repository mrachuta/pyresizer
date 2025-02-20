import platform
import subprocess
import unittest


class TestE2E(unittest.TestCase):

    def setUp(self):
        self.subprocess_required_args = {
            "cwd": "dist",
            "capture_output": True,
            "text": True,
        }
        if platform.system() == "Windows":
            self.executable = "pyresizer.exe"
        elif platform.system() == "Linux":
            self.executable = "pyresizer"
        else:
            raise SystemError("Error: cannot continue E2E tests. Unsupported platform.")

    def testHelp(self):
        result = subprocess.run(
            [self.executable, "--help"], **self.subprocess_required_args
        )
        self.assertIn("Type -h or --help to see more information.", result.stdout)

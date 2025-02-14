import io
import sys
import unittest
from unittest.mock import MagicMock, patch

from pyresizer import InstallerUninstaller, Resizer

# Unit tests generated with support of DeepSeek AI


class TestResizer(unittest.TestCase):

    def setUp(self):
        # Setup code that runs before each test
        self.new_width = 800
        self.new_height = 600
        self.resizer = Resizer(self.new_width, self.new_height)

    def tearDown(self):
        # Stop all patches after each test
        patch.stopall()

    def test_initialization(self):
        self.assertEqual(self.resizer.img_dims, (self.new_width, self.new_height))
        self.assertEqual(
            self.resizer.img_formats, [".bmp", ".gif", ".jpg", ".jpeg", ".png"]
        )
        self.assertEqual(self.resizer.bak_folder, "bak")

    def test_initialization_with_no_arguments(self):
        with self.assertRaises(TypeError):
            Resizer()

    @patch("pyresizer.os_listdir")
    @patch("pyresizer.os_path.isfile")
    def test_get_imgs(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = [
            "test.bmp",
            "test.gif",
            "test.jpg",
            "test.txt",
            "test.png",
        ]
        # Simulate that all files are valid files
        mock_isfile.side_effect = lambda x: True

        imgs = self.resizer.get_imgs

        self.assertEqual(imgs, ["test.bmp", "test.gif", "test.jpg", "test.png"])

    @patch("pyresizer.os_listdir")
    @patch("pyresizer.os_path.isfile")
    def test_get_imgs_no_images(self, mock_isfile, mock_listdir):

        mock_listdir.return_value = ["test.txt", "test.doc", "test.pdf"]
        mock_isfile.side_effect = lambda x: True

        imgs = self.resizer.get_imgs

        self.assertEqual(imgs, [])

    @patch("pyresizer.os_path.exists")
    @patch("pyresizer.os_mkdir")
    @patch("pyresizer.shutil_copy2")
    @patch("pyresizer.os_listdir")
    @patch("pyresizer.os_path.isfile")
    def test_make_backups_success(
        self, mock_isfile, mock_listdir, mock_copy2, mock_mkdir, mock_exists
    ):

        mock_listdir.return_value = ["test.bmp", "test.gif", "test.jpg", "test.png"]
        mock_isfile.side_effect = lambda x: True
        mock_exists.return_value = False

        result = self.resizer.make_backups()

        # Assert that the backup folder was created
        mock_mkdir.assert_called_once_with(self.resizer.bak_folder)
        # Assert that shutil_copy2 was called for each image
        self.assertEqual(mock_copy2.call_count, len(self.resizer.get_imgs))

        self.assertTrue(result)

    @patch("pyresizer.os_path.exists")
    @patch("pyresizer.os_mkdir")
    @patch("pyresizer.shutil_copy2")
    @patch("pyresizer.os_listdir")
    @patch("pyresizer.os_path.isfile")
    @patch("builtins.input", lambda *args: "n")
    def test_make_backups_failure(
        self, mock_isfile, mock_listdir, mock_copy2, mock_mkdir, mock_exists
    ):
        mock_listdir.return_value = ["test.bmp", "test.gif", "test.jpg", "test.png"]
        mock_isfile.side_effect = lambda x: True
        # Simulate that the backup folder does not exist initially
        mock_exists.return_value = False
        # Simulate an IOError during the backup process
        mock_copy2.side_effect = IOError("Backup failed")

        result = self.resizer.make_backups()

        mock_mkdir.assert_called_once_with(self.resizer.bak_folder)

        self.assertFalse(result)

    @patch("pyresizer.os_listdir")
    @patch("pyresizer.os_path.isfile")
    @patch("pyresizer.pil_open")
    @patch("pyresizer.shutil_copy2")
    @patch("pyresizer.os_path.exists")
    @patch("pyresizer.os_mkdir")
    def test_resize_files_success(
        self,
        mock_mkdir,
        mock_exists,
        mock_copy2,
        mock_pil_open,
        mock_isfile,
        mock_listdir,
    ):

        mock_listdir.return_value = ["test.jpg", "test.png"]
        mock_isfile.side_effect = lambda x: True

        mock_exists.return_value = False
        # Mock the PIL image object
        mock_image = MagicMock()
        mock_pil_open.return_value = mock_image
        # Mock the Resampling.LANCZOS value
        mock_resampling = MagicMock()
        mock_resampling.LANCZOS = 1  # Simulate the actual value of Resampling.LANCZOS
        mock_pil_open.return_value.Resampling = mock_resampling

        # Call the resize_files method
        result = self.resizer.resize_files()

        mock_mkdir.assert_called_once_with(self.resizer.bak_folder)

        self.assertEqual(mock_copy2.call_count, len(self.resizer.get_imgs))
        # Assert that the image was resized and saved for each image
        self.assertEqual(mock_image.thumbnail.call_count, len(self.resizer.get_imgs))
        for call in mock_image.thumbnail.call_args_list:
            self.assertEqual(
                call, unittest.mock.call(self.resizer.img_dims, mock_resampling.LANCZOS)
            )

        self.assertTrue(result)

    @patch("pyresizer.os_listdir")
    @patch("pyresizer.os_path.isfile")
    @patch("pyresizer.pil_open")
    @patch("pyresizer.shutil_copy2")
    @patch("pyresizer.os_path.exists")
    @patch("pyresizer.os_mkdir")
    def test_resize_files_failure(
        self,
        mock_mkdir,
        mock_exists,
        mock_copy2,
        mock_pil_open,
        mock_isfile,
        mock_listdir,
    ):

        mock_listdir.return_value = ["test.jpg", "test.png"]
        mock_isfile.side_effect = lambda x: True
        mock_exists.return_value = False

        mock_pil_open.side_effect = IOError("Resizing failed")

        # Call the resize_files method and expect an IOError
        with self.assertRaises(IOError) as context:
            self.resizer.resize_files()

        mock_mkdir.assert_called_once_with(self.resizer.bak_folder)
        # Assert that the correct error message was raised
        self.assertEqual(
            str(context.exception), "Error: some files were not processed!"
        )


class TestInstallerUninstaller(unittest.TestCase):

    @patch("pyresizer.sys")
    @patch("pyresizer.platform")
    def setUp(self, mock_platform, mock_sys):

        mock_sys.frozen = True
        mock_platform.system.return_value = "Windows"
        self.installeruninstaller = InstallerUninstaller("testapp")

    def tearDown(self):

        patch.stopall()

    @patch("pyresizer.sys")
    def test_initialization_not_frozen(self, mock_sys):

        mock_sys.frozen = False
        with self.assertRaises(SystemError) as context:
            # Initialize object again
            InstallerUninstaller("testapp")
        self.assertEqual(
            str(context.exception),
            "Error: cannot install Python file because of dependecies.",
        )

    @patch("pyresizer.platform")
    def test_initialization_with_no_arguments(self, mock_platform):

        mock_platform.system.return_value = "Darwin"
        # Test that creating a Resizer object with no arguments raises a TypeError
        with self.assertRaises(TypeError):
            InstallerUninstaller()

    @patch("pyresizer.sys")
    @patch("pyresizer.platform")
    def test_initialization_unsupported_platform(self, mock_platform, mock_sys):

        mock_sys.frozen = True
        mock_platform.system.return_value = "Darwin"
        with self.assertRaises(SystemError) as context:
            InstallerUninstaller("pyresizer")
        self.assertEqual(
            str(context.exception),
            "Error: cannot continue installation. Unsupported platform.",
        )

    @patch("pyresizer.platform")
    def test_copy_file_unsupported_platform(self, mock_platform):

        mock_platform.system.return_value = "Darwin"
        # Use already initialized object
        installer = self.installeruninstaller
        with self.assertRaises(SystemError) as context:
            installer.copy_file()
        self.assertEqual(
            str(context.exception),
            "Error: cannot continue installation. Unsupported platform.",
        )

    @patch("pyresizer.os_path")
    @patch("pyresizer.shutil_copy2")
    def test_copy_file_io_error(self, mock_copy2, mock_os_path):

        mock_os_path.exists.return_value = False
        mock_copy2.side_effect = IOError("File copy failed")
        installer = self.installeruninstaller
        with self.assertRaises(IOError) as context:
            installer.copy_file()
        self.assertEqual(str(context.exception), "Error: executable file not copied!")

    @patch("pyresizer.platform")
    def test_remove_file_unsupported_platform(self, mock_platform):

        mock_platform.system.return_value = "Darwin"
        installer = self.installeruninstaller
        with self.assertRaises(SystemError) as context:
            installer.remove_file()
        self.assertEqual(
            str(context.exception),
            "Error: cannot continue uninstallation. Unsupported platform.",
        )

    @patch("pyresizer.platform")
    @patch("pyresizer.os_path")
    @patch("pyresizer.shutil_rmtree")
    def test_remove_file_os_error_windows(
        self, mock_rmtree, mock_os_path, mock_platform
    ):

        # Mock again because of second if
        mock_platform.system.return_value = "Windows"
        mock_os_path.exists.return_value = True
        mock_rmtree.side_effect = OSError("Directory removal failed")
        installer = self.installeruninstaller
        with self.assertRaises(OSError) as context:
            installer.remove_file()
        self.assertEqual(
            str(context.exception),
            "Error: subdirectory together with executable file not removed!",
        )

    @patch("pyresizer.platform")
    @patch("pyresizer.os_path")
    @patch("pyresizer.shutil_rmtree")
    def test_remove_file_os_error_linux(self, mock_rmtree, mock_os_path, mock_platform):

        mock_platform.system.return_value = "Linux"
        mock_os_path.exists.return_value = True
        mock_rmtree.side_effect = OSError("Directory removal failed")
        installer = self.installeruninstaller
        with self.assertRaises(OSError) as context:
            installer.remove_file()
        self.assertEqual(str(context.exception), "Error: executable file not removed!")


if __name__ == "__main__":
    unittest.main()

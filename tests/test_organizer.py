import os
import tempfile
import unittest

from src.organizer import build_plan, get_category, get_unique_path

class TestOrganizer(unittest.TestCase):
    def test_category_detection(self):
        self.assertEqual(get_category("document.pdf"), "Documents")
        self.assertEqual(get_category("image.jpg"), "Images")
        self.assertEqual(get_category("video.mp4"), "Videos")
        self.assertEqual(get_category("unknown.xyz"), "Other")
        self.assertEqual(get_category("audio.mp3"), "Audio")
        self.assertEqual(get_category("archive.zip"), "Archives")
        self.assertEqual(get_category("script.py"), "Programs")
        self.assertEqual(get_category("spreadsheet.xlsx"), "Spreadsheets")

    def test_uppercase_extensions(self):
        self.assertEqual(get_category("DOCUMENT.PDF"), "Documents")
                         
    def test_unknown_extension(self):
        self.assertEqual(get_category("file.unknown"), "Other")

    def test_file_without_extension(self):
        self.assertEqual(get_category("file"), "Other")

    def test_build_plan(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            filenames = [
                "image.jpg", "document.pdf", "video.mp4",
                "audio.mp3", "archive.zip", "script.py",
                "spreadsheet.xlsx", "unknown.xyz"
            ]

            for filename in filenames:
                path = os.path.join(temp_dir, filename)
                with open(path, 'w') as f:
                    f.write("Test")

            plan = build_plan(temp_dir)

            self.assertIn("Images", plan)
            self.assertIn("Documents", plan)
            self.assertIn("Videos", plan)
            self.assertIn("Audio", plan)
            self.assertIn("Archives", plan)
            self.assertIn("Programs", plan)
            self.assertIn("Spreadsheets", plan)
            self.assertIn("Other", plan)

    def test_unique_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a file to test unique path generation
            original_path = os.path.join(temp_dir, "file.txt")
            with open(original_path, 'w', encoding='utf-8') as f:
                f.write("Test")

            # Generate a unique path for the same filename
            unique_path = get_unique_path(temp_dir, filename="file.txt")

            self.assertNotEqual(original_path, unique_path)
            self.assertTrue(unique_path.startswith(os.path.join(temp_dir, "file")))
            self.assertTrue(unique_path.endswith(".txt"))

if __name__ == "__main__":
    unittest.main()
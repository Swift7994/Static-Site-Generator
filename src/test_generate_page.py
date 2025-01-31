import unittest
from generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        markdown = "# My Title\nSome content."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_multiple_headings(self):
        markdown = "# First Title\n## Subtitle\n# Another Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_no_title(self):
        markdown = "## Subtitle\nSome content."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_empty_string(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_title_with_whitespace(self):
        markdown = "#    Whitespace Title     \nContent."
        self.assertEqual(extract_title(markdown), "Whitespace Title")

    def test_only_hashes(self):
        markdown = "#\nContent."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_title_with_inline_formatting(self):
        markdown = "# **Bold Title**\nContent."
        self.assertEqual(extract_title(markdown), "**Bold Title**")

if __name__ == "__main__":
    unittest.main()
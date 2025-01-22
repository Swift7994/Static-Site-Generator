import unittest
from markdown_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        markdown = "This is a single block of text."
        expected = ["This is a single block of text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_blocks(self):
        markdown = "First block.\n\nSecond block.\n\nThird block."
        expected = ["First block.", "Second block.", "Third block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_trailing_and_leading_whitespace(self):
        markdown = "   First block.   \n\n   Second block.   "
        expected = ["First block.", "Second block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_only_whitespace(self):
        markdown = "   \n\n   "
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_blocks_with_empty_lines_between(self):
        markdown = "Block one.\n\n\n\nBlock two."
        expected = ["Block one.", "Block two."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_block_with_extra_newlines(self):
        markdown = "\n\nSingle block.\n\n"
        expected = ["Single block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_special_characters(self):
        markdown = "Block with **bold** text.\n\nAnother block with *italic* text."
        expected = ["Block with **bold** text.", "Another block with *italic* text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_newlines_at_end(self):
        markdown = "First block.\n\nSecond block.\n\n\n\n"
        expected = ["First block.", "Second block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)
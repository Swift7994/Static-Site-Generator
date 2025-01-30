import unittest
from markdown_blocks import *


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


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading")
        self.assertNotEqual(block_to_block_type("####### Invalid heading"), "heading")
        self.assertNotEqual(block_to_block_type("#Invalid"), "heading")

    def test_code(self):
        self.assertEqual(block_to_block_type("```\nprint('Hello')\n```"), "code")
        self.assertNotEqual(block_to_block_type("```print('Hello')```"), "code")  # No newline in the block
        self.assertNotEqual(block_to_block_type("```\n```"), "code")  # Empty code block

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), "quote")
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), "quote")
        self.assertNotEqual(block_to_block_type("This is not a quote"), "quote")

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), "unordered_list")
        self.assertNotEqual(block_to_block_type("* Item 1\n- Item 2"), "unordered_list")  # Mixed markers

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), "ordered_list")
        self.assertNotEqual(block_to_block_type("1. Item 1\n3. Item 2"), "ordered_list")  # Out of order
        self.assertNotEqual(block_to_block_type("Item 1\nItem 2"), "ordered_list")  # No numbers

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), "paragraph")
        self.assertEqual(block_to_block_type("Just some random text."), "paragraph")


class TestIsHeading(unittest.TestCase):
    def test_valid_headings(self):
        self.assertTrue(is_heading("# Heading 1"))
        self.assertTrue(is_heading("###### Heading 6"))
    
    def test_invalid_headings(self):
        self.assertFalse(is_heading("####### Invalid heading"))  # Too many `#`
        self.assertFalse(is_heading("#Invalid"))  # No space after `#`
        self.assertFalse(is_heading("Not a heading"))  # Does not start with `#`


class TestIsCode(unittest.TestCase):
    def test_valid_code_blocks(self):
        self.assertTrue(is_code("```\nprint('Hello')\n```"))
        self.assertTrue(is_code("```\nCode with multiple lines\nprint('Hello')\n```"))

    def test_invalid_code_blocks(self):
        self.assertFalse(is_code("```print('Hello')```"))  # No newline
        self.assertFalse(is_code("```\n```"))  # Empty code block
        self.assertFalse(is_code("`Not a code block`"))  # Single backticks


class TestIsQuote(unittest.TestCase):
    def test_valid_quotes(self):
        self.assertTrue(is_quote("> This is a quote"))
        self.assertTrue(is_quote("> Line 1\n> Line 2"))

    def test_invalid_quotes(self):
        self.assertFalse(is_quote("This is not a quote"))
        self.assertFalse(is_quote("> Mixed\nLine"))  # Not all lines start with `>`


class TestIsUnorderedList(unittest.TestCase):
    def test_valid_unordered_lists(self):
        self.assertTrue(is_unordered_list("* Item 1\n* Item 2"))
        self.assertTrue(is_unordered_list("- Item 1\n- Item 2"))

    def test_invalid_unordered_lists(self):
        self.assertFalse(is_unordered_list("* Item 1\n- Item 2"))  # Mixed markers
        self.assertFalse(is_unordered_list("Item 1\nItem 2"))  # No markers


class TestIsOrderedList(unittest.TestCase):
    def test_valid_ordered_lists(self):
        self.assertTrue(is_ordered_list("1. Item 1\n2. Item 2"))
        self.assertTrue(is_ordered_list("1. First\n2. Second\n3. Third"))

    def test_invalid_ordered_lists(self):
        self.assertFalse(is_ordered_list("1. Item 1\n3. Item 2"))  # Out of order
        self.assertFalse(is_ordered_list("Item 1\nItem 2"))  # No numbers
        self.assertFalse(is_ordered_list("1. Item\nSecond item"))  # Inconsistent formatting


class TestMarkdownToHtml(unittest.TestCase):

    def test_paragraph_to_html_node(self):
        block = "This is a paragraph."
        result = paragraph_to_html_node(block)
        self.assertEqual(result.tag, "p")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].value, "This is a paragraph.")

    def test_heading_to_html_node(self):
        block = "### Heading Level 3"
        result = heading_to_html_node(block)
        self.assertEqual(result.tag, "h3")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].value, "Heading Level 3")

    def test_heading_to_html_node_invalid_level(self):
        block = "####### Invalid Heading"
        with self.assertRaises(ValueError):
            heading_to_html_node(block)

    def test_code_to_html_node_invalid(self):
        block = "`print('Missing backticks')`"
        with self.assertRaises(ValueError):
            code_to_html_node(block)

    def test_quote_to_html_node(self):
        block = "> This is a quote.\n> It spans multiple lines."
        result = quote_to_html_node(block)
        self.assertEqual(result.tag, "blockquote")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].value, "This is a quote. It spans multiple lines.")

    def test_unordered_list_to_html_node(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = unordered_list_to_html_node(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "li")
        self.assertEqual(result.children[0].children[0].value, "Item 1")
        self.assertEqual(result.children[1].children[0].value, "Item 2")
        self.assertEqual(result.children[2].children[0].value, "Item 3")

    def test_ordered_list_to_html_node(self):
        block = "1. Step 1\n2. Step 2\n3. Step 3"
        result = ordered_list_to_html_node(block)
        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "li")
        self.assertEqual(result.children[0].children[0].value, "Step 1")
        self.assertEqual(result.children[1].children[0].value, "Step 2")
        self.assertEqual(result.children[2].children[0].value, "Step 3")

    def test_process_block(self):
        block = "This is a test block."
        result = process_block(block, "div")
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].value, "This is a test block.")

    def test_markdown_to_html_node(self):
        markdown = """# Title\n\nThis is a paragraph.\n\n- Item 1\n- Item 2"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[0].children[0].value, "Title")
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(result.children[1].children[0].value, "This is a paragraph.")
        self.assertEqual(result.children[2].tag, "ul")
        self.assertEqual(result.children[2].children[0].tag, "li")
        self.assertEqual(result.children[2].children[0].children[0].value, "Item 1")


if __name__ == "__main__":
    unittest.main()
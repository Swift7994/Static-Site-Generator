import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_text_node_equality(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.TEXT)
        node3 = TextNode("Hi", TextType.TEXT)
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

    def test_text_node_repr(self):
        node = TextNode("Hello", TextType.BOLD, None)
        expected_repr = "TextNode('Hello', bold)"
        self.assertEqual(repr(node), expected_repr)

    def test_text_node_to_html_text(self):
        text_node = TextNode("Hello", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(None, "Hello")
        self.assertEqual(html_node, expected_html_node)

    def test_text_node_to_html_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("b", "Bold text")
        self.assertEqual(html_node, expected_html_node)

    def test_text_node_to_html_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("i", "Italic text")
        self.assertEqual(html_node, expected_html_node)

    def test_text_node_to_html_code(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("code", "Code text")
        self.assertEqual(html_node, expected_html_node)

    def test_text_node_to_html_link(self):
        text_node = TextNode("somewebsite.com", TextType.LINK, "https://somewebsite.com")
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("a", "somewebsite.com", {"href": "https://somewebsite.com"})
        self.assertEqual(html_node, expected_html_node)

    def test_text_node_to_html_image(self):
        text_node = TextNode("somewebsite Logo", TextType.IMAGE, "https://somewebsite.com/")
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("img", "", {"src": "https://somewebsite.com/", "alt": "somewebsite Logo"})
        self.assertEqual(html_node, expected_html_node)

    def test_invalid_text_type(self):
        text_node = TextNode("Invalid", "unknown")  # Not part of TextType Enum
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Invalid text type")



if __name__ == "__main__":
    unittest.main()

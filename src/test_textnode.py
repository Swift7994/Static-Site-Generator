import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test2_eq(self):
        node = TextNode("This is another text node", TextType.ITALIC, None)
        node2 = TextNode("This is another text node", TextType.ITALIC, None)
        self.assertEqual(node, node2)

    def test3_eq(self):
        node = TextNode("", TextType.BOLD, "https://www.hotsinglesnearyou.com")
        node2 = TextNode("", TextType.BOLD, "https://www.hotsinglesnearyou.com")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()

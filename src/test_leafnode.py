import unittest
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = LeafNode("span", "Hello", {"class": "greeting"})
        node2 = LeafNode("span", "Hello", {"class": "greeting"})
        node3 = LeafNode("span", "Hi", {"class": "greeting"})
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

    def test_init(self):
        node = LeafNode("span", "Hello, World!", {"class": "greeting"})
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.props, {"class": "greeting"})
        self.assertEqual(node.children, [])
        self.assertEqual(node.to_html(), '<span class="greeting">Hello, World!</span>')

    def test_props(self):
        leaf = LeafNode("p", "This is a paragraph.")
        self.assertEqual(leaf.props, {})
        self.assertEqual(leaf.to_html(), "<p>This is a paragraph.</p>")

    def test_value(self):
        with self.assertRaises(ValueError):
            LeafNode("span", None, {"class": "error"})

    def test_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_add_children(self):
        node = LeafNode("span", "Hello, World!", {"class": "greeting"})
        with self.assertRaises(AttributeError):
            node.children = ["child1"]
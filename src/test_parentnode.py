import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode("i", "Italic")
        node1 = ParentNode("div", [child1, child2], {"class": "container"})
        node2 = ParentNode("div", [child1, child2], {"class": "container"})
        node3 = ParentNode("div", [child1], {"class": "container"})
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

    def test_to_html(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode("i", "Italic")
        node = ParentNode("div", [child1, child2], {"class": "container"})
        expected_html = '<div class="container"><b>Bold</b><i>Italic</i></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_nested(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode("i", "Italic")
        nested = ParentNode("span", [child1], {"class": "highlight"})
        node = ParentNode("div", [nested, child2], {"class": "container"})
        expected_html = '<div class="container"><span class="highlight"><b>Bold</b></span><i>Italic</i></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_empty_children(self):
        node = ParentNode("div", [], {"class": "empty"})
        expected_html = '<div class="empty"></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_no_tag_error(self):
        child1 = LeafNode("b", "Bold")
        with self.assertRaises(ValueError):
            node = ParentNode(None, [child1])
            node.to_html()

    def test_no_children_error(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()

    def test_repr(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode("i", "Italic")
        node = ParentNode("div", [child1, child2], {"class": "container"})
        expected_repr = "ParentNode(div, children: [LeafNode(b, Bold, None), LeafNode(i, Italic, None)], {'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)

    def test_add_invalid_child(self):
        with self.assertRaises(AttributeError):
            node = ParentNode("div", "not list")
            node.children = "Children must be a list"

    def test_repr_with_none_props(self):
        child1 = LeafNode("b", "Bold")
        node_with_none_props = ParentNode("div", [child1], None)
        expected_repr_none = "ParentNode(div, children: [LeafNode(b, Bold, None)], None)"
        self.assertEqual(repr(node_with_none_props), expected_repr_none)

    def test_repr_with_empty_props(self):
        child1 = LeafNode("b", "Bold")
        node_with_empty_props = ParentNode("div", [child1], {})
        expected_repr_empty = "ParentNode(div, children: [LeafNode(b, Bold, None)], {})"
        self.assertEqual(repr(node_with_empty_props), expected_repr_empty)

    def test_recursive_no_nesting(self):
        node = ParentNode("div", [])
        expected_html = '<div></div>'
        expected_repr = "ParentNode(div, children: [], None)"
        self.assertEqual(node.to_html(), expected_html)
        self.assertEqual(repr(node), expected_repr)



if __name__ == "__main__":
    unittest.main()
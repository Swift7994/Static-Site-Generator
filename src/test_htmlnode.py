import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode(tag="div", value="Hello", children=None, props={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_equality_same_node(self):
        node1 = HTMLNode(tag="p", value="Hello", children=None, props={"class": "text"})
        node2 = HTMLNode(tag="p", value="Hello", children=None, props={"class": "text"})
        self.assertEqual(node1, node2)

    def test_equality_different_node(self):
        node1 = HTMLNode(tag="p", value="Hello", children=None, props={"class": "text"})
        node2 = HTMLNode(tag="div", value="Hello", children=None, props={"class": "text"})
        self.assertNotEqual(node1, node2)

    def test_equality_with_non_htmlnode(self):
        node = HTMLNode(tag="p", value="Hello", children=None, props={"class": "text"})
        self.assertNotEqual(node, "not a node")

    def test_repr(self):
        node = HTMLNode(tag="span", value="Content", children=None, props={"style": "color: red;"})
        expected_repr = "HTMLNode(span, Content, children: None, {'style': 'color: red;'})"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="div", value="Some value")
        with self.assertRaises(NotImplementedError):
            node.to_html()



if __name__ == "__main__":
    unittest.main()
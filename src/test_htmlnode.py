import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test2_not_eq(self):
        node = HTMLNode("test tag", "test value")
        node2 = HTMLNode("test tag", "test AAvalue")
        self.assertNotEqual(node, node2)

    def test3_eq(self):
        node = HTMLNode("a", "Click here", children=None, props={"href": "https://www.example.com", "target": "_blank"})
        node2 = HTMLNode("a", "Click here", children=None, props={"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(node, node2)

    def test4_eq(self):
        node = HTMLNode(tag="ul", value=None, children=[
        HTMLNode(tag="li", value="Item 1", children=None, props=None),
        HTMLNode(tag="li", value="Item 2", children=None, props=None),
    ], 
    props=None)
        node2 = HTMLNode(tag="ul", value=None, children=[
        HTMLNode(tag="li", value="Item 1", children=None, props=None),
        HTMLNode(tag="li", value="Item 2", children=None, props=None),
    ], 
    props=None)
        self.assertEqual(node, node2)



if __name__ == "__main__":
    unittest.main()
import unittest
from textnode import TextType, TextNode
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_simple(self):
        nodes = [TextNode("Hello *bold* world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" world", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(result, nodes)

    def test_multiple_delimiters(self):
        nodes = [TextNode("This is *bold* and *italic*", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_uneven_delimiters(self):
        nodes = [TextNode("This is *missing end delimiter", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(str(context.exception), "Missing closing delimiter")

    def test_non_text_nodes(self):
        nodes = [
            TextNode("Hello *bold* world", TextType.TEXT),
            TextNode("Link", TextType.LINK, url="http://example.com"),
        ]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" world", TextType.TEXT),
            TextNode("Link", TextType.LINK, url="http://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiter_pairs(self):
        nodes = [TextNode("text *code* more *code* end", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.CODE)
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" more ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_delimiter_pairs(self):
        nodes = [TextNode("text ** empty ** end", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "*", TextType.BOLD)
            self.assertEqual(str(context.exception), "Empty delimited section is not allowed")

    def test_uneven_delimiters(self):
        nodes = [TextNode("text *missing end delimiter", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(str(context.exception), "Missing closing delimiter")

    def test_non_text_nodes(self):
        nodes = [
            TextNode("text *bold* text", TextType.TEXT),
            TextNode("Link", TextType.LINK, url="http://example.com"),
        ]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("Link", TextType.LINK, url="http://example.com"),
        ]
        self.assertEqual(result, expected)

class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        nodes = [TextNode("Here is an image ![example](https://example.com/image.png).", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("example", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        nodes = [
            TextNode(
                "This contains ![image1](https://example.com/img1.png) and ![image2](https://example.com/img2.png).",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This contains ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://example.com/img1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/img2.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        nodes = [TextNode("This text has no images.", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [TextNode("This text has no images.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_empty_input(self):
        nodes = []
        result = split_nodes_image(nodes)
        expected = []
        self.assertEqual(result, expected)

    def test_empty_text_node(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = []
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        nodes = [
            TextNode("Here is an image ![example](https://example.com/image.png).", TextType.TEXT),
            TextNode("Unchanged node", TextType.IMAGE, "https://example.com/other_image.png"),
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("example", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.TEXT),
            TextNode("Unchanged node", TextType.IMAGE, "https://example.com/other_image.png"),
        ]
        self.assertEqual(result, expected)

    def test_unclosed_image(self):
        nodes = [TextNode("Here is an ![incomplete image(https://example.com/image.png).", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [TextNode("Here is an ![incomplete image(https://example.com/image.png).", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_image_without_alt_text(self):
        nodes = [TextNode("Here is an image ![](https://example.com/image.png).", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_special_characters_in_image_url(self):
        nodes = [
            TextNode(
                "Here is an image ![special](https://example.com/image_with-special_chars?foo=bar&baz=qux).",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("special", TextType.IMAGE, "https://example.com/image_with-special_chars?foo=bar&baz=qux"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_large_input(self):
        text = " ".join([f"This is an ![image{i}](https://example{i}.com/image.png)" for i in range(100)])
        nodes = [TextNode(text, TextType.TEXT)]
        result = split_nodes_image(nodes)

        # Expected: 100 images, with alternating text nodes
        self.assertEqual(len(result), 200)
        self.assertEqual(result[0], TextNode("This is an ", TextType.TEXT))
        self.assertEqual(result[-1], TextNode("image99", TextType.IMAGE, "https://example99.com/image.png"))

class TestSplitNodesLink(unittest.TestCase):

    def test_single_markdown_link(self):
        nodes = [TextNode("This is a [link](https://example.com).", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_markdown_links(self):
        nodes = [
            TextNode(
                "Here is a [link1](https://example.com) and another [link2](https://example2.com).",
                TextType.TEXT,
            )
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example2.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_markdown_links(self):
        nodes = [TextNode("This text has no links.", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [TextNode("This text has no links.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_empty_input(self):
        nodes = []
        result = split_nodes_link(nodes)
        expected = []
        self.assertEqual(result, expected)

    def test_empty_text_node(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = []
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        nodes = [
            TextNode("This is a [link](https://example.com).", TextType.TEXT),
            TextNode("Unchanged node", TextType.LINK, "https://other.com"),
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
            TextNode("Unchanged node", TextType.LINK, "https://other.com"),
        ]
        self.assertEqual(result, expected)

    def test_unclosed_markdown_link(self):
        nodes = [TextNode("Here is an [incomplete link(https://example.com).", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [TextNode("Here is an [incomplete link(https://example.com).", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_link_without_alt_text(self):
        nodes = [TextNode("Here is a [](https://example.com).", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_special_characters_in_links(self):
        nodes = [
            TextNode(
                "Here is a [special](https://example.com/with-special_chars?foo=bar&baz=qux).",
                TextType.TEXT,
            )
        ]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("special", TextType.LINK, "https://example.com/with-special_chars?foo=bar&baz=qux"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_large_input(self):
        text = " ".join([f"This is [link{i}](https://example{i}.com)" for i in range(100)])
        nodes = [TextNode(text, TextType.TEXT)]
        result = split_nodes_link(nodes)

        # Expected: 100 links, with alternating text nodes
        self.assertEqual(len(result), 200)
        self.assertEqual(result[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(result[-1], TextNode("link99", TextType.LINK, "https://example99.com"))

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text with no formatting."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is plain text with no formatting.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text = "This is *italic* text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        text = "Here is `code`."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image(self):
        text = "Here is an image ![example](https://example.com/image.png)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("example", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link(self):
        text = "Here is a [link](https://example.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_combined_formatting(self):
        text = "This is **bold**, *italic*, and `code` with a [link](https://example.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_complex_text(self):
        text = (
            "Text with **bold** and *italic*, a `code`, an image ![alt](https://example.com/img.png), "
            "and a [link](https://example.com)."
        )
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", an image ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(", and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_text(self):
        text = ""
        result = text_to_textnodes(text)
        expected = []
        self.assertEqual(result, expected)

    def test_text_with_unclosed_formatting(self):
        text = "This is **bold and *italic with `code and a [link](https://example.com)."
        with self.assertRaises(Exception) as context:
            text_to_textnodes(text)
            self.assertEqual(str(context.exception), "Missing closing delimiter")

    def test_edge_case_with_just_formatting(self):
        text = "**bold** *italic* `code` [link](https://example.com) ![img](https://example.com/img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

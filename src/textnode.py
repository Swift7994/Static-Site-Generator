from enum import Enum
from leafnode import LeafNode

# Enum representing different types of text formatting used in Markdown.
class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


# Represents a piece of text with an associated formatting type.
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text # # The actual text content
        self.text_type = text_type # The formatting type (bold, italic, etc.)
        self.url = url # Optional URL for links or images

    # Checks if two TextNode instances are equal.
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    # Returns a string representation of the TextNode instance.
    def __repr__(self):
        if self.url is not None:
            return f"TextNode('{self.text}', {self.text_type.value}, '{self.url}')"
        else:
            return f"TextNode('{self.text}', {self.text_type.value})"


# Converts a TextNode into an HTML representation as a LeafNode.
# Based on the text type of the TextNode, it wraps the text content in the appropriate HTML element.
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Invalid text type")
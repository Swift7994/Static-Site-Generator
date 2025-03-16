from htmlnode import HTMLNode


# A class that represents a leaf node in an HTML structure.
# A leaf node is an HTML element that has a tag and a value.
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Ensure that the value for the leaf node is provided
        if value is None:
            raise ValueError("LeafNode must have a value")
        # Initialize the parent class (HTMLNode) with tag, value, no children, and optional props
        super().__init__(tag, value, None, props)

    # Converts the LeafNode to its corresponding HTML string representation.
    def to_html(self):
        # If no tag, return just the value (this could be a text node)
        if self.tag is None:
            return f"{self.value}"
        # Otherwise, return the tag-wrapped value with additional props if any.
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    # Compares two LeafNode instances for equality.
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (self.tag == other.tag and self.value == other.value and self.props == other.props)
    
    # Provides a string representation of the LeafNode instance for debugging.
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
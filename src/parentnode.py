from htmlnode import HTMLNode
from leafnode import LeafNode


# A class that represents a parent node in an HTML structure.
# A parent node is an HTML element that can have one or more children nodes. It can contain
# other elements (such as other parent nodes or leaf nodes).
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # Validate that children is a non-empty list of valid child nodes
        if children is None:
            raise ValueError("HTML must have children")
        if not isinstance(children, list):
            raise AttributeError("Children must be a list")
        for child in children:
            if not isinstance(child, (LeafNode, ParentNode)):
                raise AttributeError("Each child must be a LeafNode or ParentNode")
        # Call the parent (HTMLNode) constructor
        super().__init__(tag, None, children, props)
    
    # Converts the ParentNode (and its children) to an HTML string representation
    def to_html(self):
        if self.tag is None:
            raise ValueError("HTML must have a tag")
        # Collect the HTML string for each child node
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        # Return the full HTML string for the parent node, including its children
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    # Provides a string representation of the ParentNode instance for debugging.
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


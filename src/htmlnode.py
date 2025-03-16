# A base class representing an HTML node. This class is intended to be inherited by other node types
# like LeafNode and ParentNode. It provides basic functionality for handling the HTML tag, value, 
# children, and properties of an HTML element.
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # This is an abstract method that must be implemented by subclasses (LeafNode, ParentNode).
    def to_html(self):
        raise NotImplementedError("method must be overridden")
    
    # Converts the node's properties (attributes) into an HTML attribute string.
    def props_to_html(self):
        html = ""
        if self.props is None:
            return html
        for key, value in self.props.items():
            html += f' {key}="{value}"'
        return html
    
    # Compares two HTMLNode instances for equality.
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props)
    
    # Returns a string representation of the HTMLNode instance.
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if children is None:
            raise ValueError("HTML must have children")
        if not isinstance(children, list):
            raise AttributeError("Children must be a list")
        for child in children:
            if not isinstance(child, (LeafNode, ParentNode)):
                raise AttributeError("Each child must be a LeafNode or ParentNode")
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("HTML must have a tag")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


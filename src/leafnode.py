from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        self._children = []
        super().__init__(tag=tag, value=value, props=props)

    @property
    def children(self):
        return []

    @children.setter
    def children(self, value):
        if value != []:
            raise AttributeError("LeafNode does not support children.")
        self._children = []

    def to_html(self):
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (self.tag == other.tag and self.value == other.value and self.props == other.props)
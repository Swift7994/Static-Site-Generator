class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html = ""
        if not self.props:
            return html
        for key, value in self.props.items():
            html += f' {key}="{value}"'
        return html
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props)
    
    def __repr__(self):
        if not self.children:
            children_repr = []
        else:
            children_repr = [repr(child) for child in self.children] if self.children else []
        return f"HTMLNode('{self.tag}', {self.value}, '{children_repr}', '{self.props}')"
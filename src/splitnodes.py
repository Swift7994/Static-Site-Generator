from textnode import TextType, TextNode
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def split_text(text):
        parts = text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Missing closing delimiter")
        nodes = [
            TextNode(part, text_type if i % 2 else TextType.TEXT)
            for i, part in enumerate(parts)
        ]
        return nodes
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.value:
            new_nodes.append(node)
            continue

        new_nodes.extend(split_text(node.value))

    return new_nodes


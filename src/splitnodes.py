from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        delimiter_count = 0
        for char in node.value:
            if char == delimiter:
                delimiter_count += 1
        if delimiter_count == 0:
            new_nodes.append(node)
            continue
        if delimiter_count % 2 != 0:
            raise Exception("Missing closing delimiter")
        split_string = node.value.split(delimiter)
        split_nodes = []
        for i, text in enumerate(split_string):
            if i % 2 == 0:
                split_nodes.append(TextNode(text, TextType.TEXT))
            else:
                split_nodes.append(TextNode(text, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
        



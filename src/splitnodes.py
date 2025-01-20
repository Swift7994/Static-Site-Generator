from textnode import TextType, TextNode
import re
        
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

        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        new_nodes.extend(split_text(node.text))

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]\\]*(?:\\.[^\[\]\\]*)*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def is_image_or_link(markdown_text):
    image_pattern = r"!\[.*?\]\(.*?\)"
    link_pattern = r"\[.*?\]\(.*?\)"
    
    if re.search(image_pattern, markdown_text):
        return "Image"
    elif re.search(link_pattern, markdown_text):
        return "Link"
    else:
        return "Invalid Markdown"
        
def split_nodes_image(old_nodes):
    def split_text(text, markdown_data):
        nodes = []
        if len(markdown_data) == 0:
            if text:
                nodes.append(TextNode(text, TextType.TEXT))
            return nodes
        current_alt = markdown_data[0][0]
        current_url = markdown_data[0][1]
        sections = text.split(f"![{current_alt}]({current_url})", 1)

        if sections[0]:
            nodes.append(TextNode(sections[0], TextType.TEXT))
        nodes.append(TextNode(current_alt, TextType.IMAGE, current_url))
        if sections[1]:
            nodes.extend(split_text(sections[1], markdown_data[1:]))
        return nodes

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text == "":
            continue

        markdown_data = extract_markdown_images(node.text)
        if markdown_data is None:
            new_nodes.append(node)
            continue

        new_nodes.extend(split_text(node.text, markdown_data))

    return new_nodes

def split_nodes_link(old_nodes):
    def split_text(text, markdown_data):
        nodes = []
        if len(markdown_data) == 0:
            if text:
                nodes.append(TextNode(text, TextType.TEXT))
            return nodes
        current_alt = markdown_data[0][0]
        current_url = markdown_data[0][1]
        sections = text.split(f"[{current_alt}]({current_url})", 1)

        if sections[0]:
            nodes.append(TextNode(sections[0], TextType.TEXT))
        nodes.append(TextNode(current_alt, TextType.LINK, current_url))
        if sections[1]:
            nodes.extend(split_text(sections[1], markdown_data[1:]))
        return nodes

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text == "":
            continue

        markdown_data = extract_markdown_links(node.text)
        if markdown_data is None:
            new_nodes.append(node)
            continue

        new_nodes.extend(split_text(node.text, markdown_data))

    return new_nodes

def text_to_textnodes(text):
    bold_nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    bold_italic_nodes = split_nodes_delimiter(bold_nodes, "*", TextType.ITALIC)
    bold_italic_code_nodes = split_nodes_delimiter(bold_italic_nodes, "`", TextType.CODE)
    bold_italic_code_link_nodes = split_nodes_image(bold_italic_code_nodes)
    split_nodes = split_nodes_link(bold_italic_code_link_nodes)
    return split_nodes
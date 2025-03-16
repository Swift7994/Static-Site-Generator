from textnode import TextType, TextNode
import re


# Splits text nodes based on a given delimiter, switching between two text types 
# (e.g., normal text and bold/italic) whenever the delimiter appears.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Splits the provided text based on the delimiter, creating a list of TextNode objects.
    def split_text(text):
        parts = text.split(delimiter)
        # Ensure the number of parts is odd (to prevent missing closing delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Missing closing delimiter")
        nodes = []
        for i, part in enumerate(parts):
            # Ensure there are no empty sections when the delimiter is inside
            if part == "" and i % 2 == 1:
                raise Exception("Empty delimited section is not allowed")
            # Skip empty sections in even-indexed parts
            if part == "" and i % 2 == 0:
                continue
            # Alternate between the provided text_type and normal text type (TextType.TEXT)
            node_type = text_type if i % 2 else TextType.TEXT
            nodes.append(TextNode(part, node_type))
        return nodes
    
    new_nodes = []
    for node in old_nodes:
        # If the node is not of type TEXT, add it to the new_nodes list without modification
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # If the delimiter is not in the node's text, add it unchanged
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        
        # If the delimiter is found, split the node's text and extend the new_nodes list with the result
        new_nodes.extend(split_text(node.text))

    return new_nodes


# Extracts all image markdown syntax from the input text and returns a list of tuples.
# This function uses a regular expression to find all occurrences of the Markdown image format:
# `![alt_text](image_url)` in the provided text.
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]\\]*(?:\\.[^\[\]\\]*)*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

# Extracts all Markdown link syntax from the input text and returns a list of tuples.
# This function uses a regular expression to find all occurrences of the Markdown link format:
# `[link_text](url)` in the provided text.
def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


# Processes a list of TextNode objects and splits the nodes when image Markdown syntax is found.
# This function identifies image Markdown (`![alt_text](image_url)`) in the text of TextNode objects,
# and splits the content into separate TextNode objects: normal text and image nodes.
def split_nodes_image(old_nodes):
    # Splits a given text into TextNode objects based on Markdown image syntax.
    def split_text(text, markdown_data):
        nodes = []
        # If no Markdown image data is provided, return the text as a single node
        if len(markdown_data) == 0:
            if text:
                nodes.append(TextNode(text, TextType.TEXT))
            return nodes
        # Extract the alt text and URL of the first image
        current_alt = markdown_data[0][0]
        current_url = markdown_data[0][1]
        # Split the text at the image Markdown syntax
        sections = text.split(f"![{current_alt}]({current_url})", 1)
        # If there's text before the image, add it as a normal text node
        if sections[0]:
            nodes.append(TextNode(sections[0], TextType.TEXT))
        # Add the image node with alt text and URL
        nodes.append(TextNode(current_alt, TextType.IMAGE, current_url))
        # If there's text after the image, recursively process the remaining text
        if sections[1]:
            nodes.extend(split_text(sections[1], markdown_data[1:]))

        return nodes

    new_nodes = []
    for node in old_nodes:
        # If the node is not a normal text node, add it to the result as is
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # Skip empty text nodes
        if node.text == "":
            continue
        # Extract image Markdown data from the text node
        markdown_data = extract_markdown_images(node.text)
        # If no image Markdown is found, add the node as is
        if markdown_data is None:
            new_nodes.append(node)
            continue
        # Otherwise, split the text node into individual nodes and add to the result
        new_nodes.extend(split_text(node.text, markdown_data))

    return new_nodes


# Processes a list of TextNode objects and splits the nodes when Markdown link syntax is found.
# This function identifies Markdown links (`[link_text](url)`) in the text of TextNode objects,
# and splits the content into separate TextNode objects for normal text and link nodes.
def split_nodes_link(old_nodes):
    # Splits a given text into TextNode objects based on Markdown link syntax.
    def split_text(text, markdown_data):
        nodes = []
        # If no Markdown link data is provided, return the text as a single node
        if len(markdown_data) == 0:
            if text:
                nodes.append(TextNode(text, TextType.TEXT))
            return nodes
        # Extract the link text and URL of the first link
        current_alt = markdown_data[0][0]
        current_url = markdown_data[0][1]
        # Split the text at the link Markdown syntax
        sections = text.split(f"[{current_alt}]({current_url})", 1)
        # If there's text before the link, add it as a normal text node
        if sections[0]:
            nodes.append(TextNode(sections[0], TextType.TEXT))
        # Add the link node with the link text and URL
        nodes.append(TextNode(current_alt, TextType.LINK, current_url))
        # If there's text after the link, recursively process the remaining text
        if sections[1]:
            nodes.extend(split_text(sections[1], markdown_data[1:]))

        return nodes

    new_nodes = []
    for node in old_nodes:
        # If the node is not a normal text node, add it to the result as is
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # Skip empty text nodes
        if node.text == "":
            continue
        # Extract Markdown link data from the text node
        markdown_data = extract_markdown_links(node.text)
        # If no link Markdown is found, add the node as is
        if markdown_data is None:
            new_nodes.append(node)
            continue
        # Otherwise, split the text node into individual nodes and add to the result
        new_nodes.extend(split_text(node.text, markdown_data))

    return new_nodes

# This function processes the input text by identifying and splitting different Markdown syntax,
# such as bold, italic, code, images, and links. It returns a list of `TextNode` objects 
# representing the text with corresponding types for each Markdown element.
def text_to_textnodes(text):
    bold_nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    bold_italic_nodes = split_nodes_delimiter(bold_nodes, "*", TextType.ITALIC)
    bold_italic_code_nodes = split_nodes_delimiter(bold_italic_nodes, "`", TextType.CODE)
    bold_italic_code_link_nodes = split_nodes_image(bold_italic_code_nodes)
    split_nodes = split_nodes_link(bold_italic_code_link_nodes)
    return split_nodes
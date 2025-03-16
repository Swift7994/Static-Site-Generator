from parentnode import ParentNode
from splitnodes import text_to_textnodes
from textnode import text_node_to_html_node


# Converts a Markdown document into a list of blocks
def markdown_to_blocks(markdown_doc):
    return [block.strip() for block in markdown_doc.split("\n\n") if block.strip()]


# This function checks the provided Markdown block against a set of predefined block types.
def block_to_block_type(markdown_block):
    block_checkers = [
        ("heading", is_heading),
        ("code", is_code),
        ("quote", is_quote),
        ("unordered_list", is_unordered_list),
        ("ordered_list", is_ordered_list),
    ]

    for block_type, checker in block_checkers:
        if checker(markdown_block):
            return block_type
    return "paragraph"
        

# Checks if the given text is a valid Markdown heading: a number of hash (`#`) characters followed by a space.
# The number of hash characters determines the level of the heading (from 1 to 6).
def is_heading(text):
    if text.startswith("#") and " " in text:
        heading_part, _ = text.split(" ", 1)
        if 1 <= len(heading_part) <= 6 and heading_part == "#" * len(heading_part):
            return True
    return False
    
# Checks if the given text is a valid Markdown code block: starts and ends with three backticks ("```") 
# and contains at least one non-empty line of code between the backticks.
def is_code(text):
    lines = text.split("\n")
    return len(lines) >= 3 and text[:3] == "```" and text[-3:] == "```" and text[3:-3].strip() != ""
        
# Checks if the given text is a valid Markdown blockquote: consists of lines where each line starts with a "> " 
# followed by the quoted content.
def is_quote(text):
    lines = text.split("\n")
    if all(line.startswith("> ") for line in lines):
        return True
    return False
    
# Checks if the given text is a valid Markdown unordered list: consists of lines where each line starts 
# with either a "* " or "- ".
def is_unordered_list(text):
    lines = text.split("\n")
    if len(lines) == 0:
        return False

    first_marker = None
    if lines[0].startswith("* "):
        first_marker = "* "
    elif lines[0].startswith("- "):
        first_marker = "- "
    else:
        return False  

    if all(line.startswith(first_marker) for line in lines):
        return True
    return False
    

# Checks if the given text is a valid Markdown ordered list: consists of lines where each line starts with a 
# number followed by a period and a space (e.g., "1. ", "2. ", "3. ").
def is_ordered_list(text):
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if not line.startswith(f"{index + 1}. "):
            return False
    return True


# Takes a Markdown document as input, processes it into blocks, converts each block into
# corresponding HTML nodes, and returns a parent HTML node that contains all the converted 
# blocks as its children.
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    # Convert each block into a corresponding HTML node using block_to_html_node
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children, None)


# Takes a Markdown block as input, determines its type (e.g., heading, code block, list, etc.), 
# and then uses the appropriate handler to convert it into an HTML node.
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    handler = block_type_handlers.get(block_type)
    if not handler:
        raise ValueError(f"Unsupported block type: {block_type}")
    return handler(block)


# Processes the input text by converting it into a list of `TextNode` objects, each representing
# a part of the text (e.g., bold, italic, code, links). Then, it converts each `TextNode` to
# its corresponding HTML node.
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


# Processes a Markdown block and converts it into an HTML element with the specified tag 
# (such as bold, italic, etc.), and wraps the resulting HTML nodes inside an HTML element
#  with the specified tag.
def process_block(block, tag):
    lines = block.split("\n")
    content = " ".join(line.strip() for line in lines)
    children = text_to_children(content)
    return ParentNode(tag, children)


# Converts a Markdown paragraph block into an HTML <p> element.
def paragraph_to_html_node(block):
    return process_block(block, "p")
# Converts a Markdown heading block into an HTML heading element (h1 to h6).
def heading_to_html_node(block):
    level = block.count("#", 0, block.find(" "))  # Count # before the first space
    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)
# Converts a Markdown code block into an HTML <pre> and <code> element.
def code_to_html_node(block):
    if not (block.startswith("```") and block.endswith("```")):
        raise ValueError("Invalid code block")
    text = block[3:-3].strip()
    children = text_to_children(text)
    code_node = ParentNode("code", children)
    return ParentNode("pre", [code_node])
# Converts a Markdown quote block into an HTML blockquote element.
def quote_to_html_node(block):
    lines = [line.lstrip(">").strip() for line in block.split("\n") if line.startswith(">")]
    return process_block("\n".join(lines), "blockquote")
# Converts a Markdown list block into an HTML list (either <ul> or <ol>) with <li> elements.
def list_to_html_node(block, tag, prefix_length):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[prefix_length:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode(tag, html_items)
# Converts a Markdown unordered list block into an HTML <ul> element.
def unordered_list_to_html_node( block):
    return list_to_html_node(block, "ul", 2)
# Converts a Markdown ordered list block into an HTML <ol> element.
def ordered_list_to_html_node(block):
    return list_to_html_node(block, "ol", 3)

# A dictionary that maps block types (e.g., paragraph, heading, code) to their respective handler functions.
block_type_handlers = {
    "paragraph": paragraph_to_html_node,
    "heading": heading_to_html_node,
    "code": code_to_html_node,
    "quote": quote_to_html_node,
    "unordered_list": unordered_list_to_html_node,
    "ordered_list": ordered_list_to_html_node,
}
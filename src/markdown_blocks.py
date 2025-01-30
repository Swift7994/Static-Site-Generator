from parentnode import ParentNode
from splitnodes import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


def markdown_to_blocks(markdown_doc):
    return [block.strip() for block in markdown_doc.split("\n\n") if block.strip()]


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
        

def is_heading(text):
    if text.startswith("#") and " " in text:
        heading_part, _ = text.split(" ", 1)
        if 1 <= len(heading_part) <= 6 and heading_part == "#" * len(heading_part):
            return True
    return False
    
    
def is_code(text):
    lines = text.split("\n")
    return len(lines) >= 3 and text[:3] == "```" and text[-3:] == "```" and text[3:-3].strip() != ""
        
    
def is_quote(text):
    lines = text.split("\n")
    if all(line.startswith("> ") for line in lines):
        return True
    return False
    
    
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
    
    
def is_ordered_list(text):
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if not line.startswith(f"{index + 1}. "):
            return False
    return True



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    handler = block_type_handlers.get(block_type)
    if not handler:
        raise ValueError(f"Unsupported block type: {block_type}")
    return handler(block)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def process_block(block, tag):
    lines = block.split("\n")
    content = " ".join(line.strip() for line in lines)
    children = text_to_children(content)
    return ParentNode(tag, children)

# Handlers for specific block types
def paragraph_to_html_node(block):
    return process_block(block, "p")

def heading_to_html_node(block):
    level = block.count("#", 0, block.find(" "))  # Count # before the first space
    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not (block.startswith("```") and block.endswith("```")):
        raise ValueError("Invalid code block")
    text = block[3:-3].strip()
    children = [TextNode(text)]  # Code blocks are treated as raw text
    code_node = ParentNode("code", children)
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = [line.lstrip(">").strip() for line in block.split("\n") if line.startswith(">")]
    return process_block("\n".join(lines), "blockquote")

def list_to_html_node(block, tag, prefix_length):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[prefix_length:].strip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode(tag, html_items)

def unordered_list_to_html_node( block):
    return list_to_html_node(block, "ul", 2)

def ordered_list_to_html_node(block):
    return list_to_html_node(block, "ol", 3)

block_type_handlers = {
    "paragraph": paragraph_to_html_node,
    "heading": heading_to_html_node,
    "code": code_to_html_node,
    "quote": quote_to_html_node,
    "unordered_list": unordered_list_to_html_node,
    "ordered_list": ordered_list_to_html_node,
}
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
    
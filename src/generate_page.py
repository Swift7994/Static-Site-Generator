from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            if title:
                return title
    raise ValueError("Title not found")

def generate_page(origin, template, destination):
    print(f"Generating HTML page from '{origin}' to '{destination}' using '{template}'.")

    with open(origin) as file:
        markdown = file.read()

    with open(template) as file:
        template_contents = file.read()

    htmlnode = markdown_to_html_node(markdown)
    html = htmlnode.to_html()

    title = extract_title(markdown)

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(destination), exist_ok=True)

    with open(destination, "w") as to_file:
        to_file.write(template_contents)

    print(f"Page successfully generated at '{destination}'.")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
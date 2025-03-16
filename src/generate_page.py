from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path


# Extracts the first level-one heading (H1) from a given Markdown string.
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("# ").strip()
            if title:
                return title
    raise ValueError("Title not found")


# Generates an HTML page from a Markdown file using a template.
def generate_page(origin, template, destination):
    print(f"Generating HTML page from '{origin}' to '{destination}' using '{template}'.")
    # Read the Markdown file
    with open(origin) as file:
        markdown = file.read()
    # Read the HTML template file
    with open(template) as file:
        template_contents = file.read()
    # Convert Markdown to HTML
    htmlnode = markdown_to_html_node(markdown)
    html = htmlnode.to_html()
    # Extract title from Markdown
    title = extract_title(markdown)
    # Replace placeholders in the template
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html)
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    # Write the generated HTML to the destination file
    with open(destination, "w") as to_file:
        to_file.write(template_contents)

    print(f"Page successfully generated at '{destination}'.")


# Recursively converts all Markdown files in a directory into HTML files 
# using a specified template and saves them in the destination directory.
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Iterate through all files and subdirectories in the given content directory
    for filename in os.listdir(dir_path_content):
        # Construct full paths for the source Markdown file and the destination HTML file
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        # Check if the current path is a file
        if os.path.isfile(from_path):
            # Change the file extension from .md (or other) to .html
            dest_path = Path(dest_path).with_suffix(".html")
            # Generate the HTML page using the given template
            generate_page(from_path, template_path, dest_path)
        else:
            # If it's a directory, call the function recursively to process its contents
            generate_pages_recursive(from_path, template_path, dest_path)
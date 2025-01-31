import os
from copystatic import copy_files
from generate_page import generate_page


path_static = "./static"
path_public = "./public"
path_content = "./content"
path_template = "./template.html"

def main():
    print("Copying static files to public directory...")
    copy_files(path_static, path_public)

    print("Generating page...")
    generate_page(
        os.path.join(path_content, "index.md"),
        path_template,
        os.path.join(path_public, "index.html"),
    )



if __name__ == "__main__":
    main()

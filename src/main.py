from copystatic import copy_files
from generate_page import generate_pages_recursive


path_static = "./static"
path_public = "./public"
path_content = "./content"
path_template = "./template.html"

def main():
    print("Copying static files to public directory...")
    copy_files(path_static, path_public)

    print("Generating content")
    generate_pages_recursive(path_content, path_template, path_public)



if __name__ == "__main__":
    main()

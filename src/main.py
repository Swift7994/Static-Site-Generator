from textnode import TextNode, TextType
from parentnode import *

def main():
    node = ParentNode("div", ["hey", "man"], {"class": "empty"})
    for child in node.children:
        print(f"debug - {child}")

if __name__ == "__main__":
    main()

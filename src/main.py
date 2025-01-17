from textnode import TextNode, TextType
from parentnode import ParentNode
from extract_alttext import extract_markdown_images

def main():
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(f"debug - {extract_markdown_images(text)}")

if __name__ == "__main__":
    main()

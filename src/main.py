from textnode import TextNode, TextType
from parentnode import ParentNode
from splitnodes import is_image_or_link

def main():
    node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
    TextType.TEXT,
)
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(f"debug - {is_image_or_link(text):}")

if __name__ == "__main__":
    main()

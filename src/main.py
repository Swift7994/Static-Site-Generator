from textnode import TextNode, TextType
from parentnode import ParentNode
from splitnodes import text_to_textnodes

def main():
    node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
    TextType.TEXT,
)
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(f"debug - {text_to_textnodes(text):}")

if __name__ == "__main__":
    main()

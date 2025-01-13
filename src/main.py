from textnode import TextNode, TextType

def main():
    dummy_node = TextNode("This is a test textnode", TextType.BOLD, "https://www.boot.dev")
    print(dummy_node)

if __name__ == "__main__":
    main()

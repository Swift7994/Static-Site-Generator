from textnode import TextNode, TextType
from splitnodes import text_to_textnodes
import unittest

class TestCount(unittest.TestCase):
    def test_count(self):
        print(f"Test discovered: {len(unittest.TestLoader().loadTestsFromTestCase(TestCount).__dict__['_tests'])}")


def main():
    node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
    TextType.TEXT)
    testcount = TestCount()
    print (testcount.test_count)
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(f"debug - ")

if __name__ == "__main__":
    main()

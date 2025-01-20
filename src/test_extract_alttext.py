import unittest
from splitnodes import extract_markdown_images, extract_markdown_links

class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is an image: ![alt text](https://example.com/image.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "https://example.com/image.png")]
        )

        text = "Images: ![img1](https://example.com/1.png) and ![img2](https://example.com/2.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("img1", "https://example.com/1.png"), ("img2", "https://example.com/2.png")]
        )

        text = "Image with empty alt text: ![](https://example.com/image.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("", "https://example.com/image.png")]
        )
        text = "Image with empty URL: ![alt text]()"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "")]
        )

        text = "Not an image: ![alt text](missing closing parenthesis"
        self.assertEqual(extract_markdown_images(text), [])

        text = "Image with escaped brackets: ![alt \\[text\\]](https://example.com/image.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt \\[text\\]", "https://example.com/image.png")]
        )

    def test_extract_markdown_links(self):
        text = "This is a [link](https://example.com)."
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://example.com")]
        )

        text = "Links: [Google](https://google.com) and [Bing](https://bing.com)."
        self.assertEqual(
            extract_markdown_links(text),
            [("Google", "https://google.com"), ("Bing", "https://bing.com")]
        )

        text = "Link with empty text: [](/path/to/resource)"
        self.assertEqual(
            extract_markdown_links(text),
            [("", "/path/to/resource")]
        )

        text = "Link with empty URL: [empty]()."
        self.assertEqual(
            extract_markdown_links(text),
            [("empty", "")]
        )

        text = "This is a [link](https://example.com) and an image ![alt](https://example.com/image.png)."
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://example.com")]
        )

        text = "Not a link: [text](missing closing parenthesis"
        self.assertEqual(extract_markdown_links(text), [])

        text = "A [complex link](https://example.com?a=1&b=2#anchor)."
        self.assertEqual(
            extract_markdown_links(text),
            [("complex link", "https://example.com?a=1&b=2#anchor")]
        )

if __name__ == "__main__":
    unittest.main()
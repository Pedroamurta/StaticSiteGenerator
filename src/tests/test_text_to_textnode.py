import unittest
from nodes.textnode import TextNode, TextType
from utils.text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "Just plain text"
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_single_bold(self):
        text = "This is **bold** text"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_single_italic(self):
        text = "An _italic_ word"
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_single_code(self):
        text = "Use the `print()` function"
        expected = [
            TextNode("Use the ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" function", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link_in_text(self):
        text = "Visit [Google](https://google.com) now"
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" now", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image_in_text(self):
        text = "A logo: ![OpenAI](logo.png)"
        expected = [
            TextNode("A logo: ", TextType.TEXT),
            TextNode("OpenAI", TextType.IMAGE, "logo.png"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_all_formats_combined(self):
        text = "Text `code` **bold** _italic_ [link](url.com) ![img](img.png)"
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "img.png"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_unmatched_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("This is **broken")


if __name__ == "__main__":
    unittest.main()

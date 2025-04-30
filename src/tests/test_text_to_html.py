import unittest
from nodes.textnode import TextNode, TextType
from utils.text_to_html import text_node_to_html_node
from nodes.leafnode import LeafNode


class TestTextToHTML(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_plain_text(self):
        tn = TextNode("Hello, world!", TextType.TEXT)
        expected = LeafNode(None, "Hello, world!")
        self.assertEqual(text_node_to_html_node(tn), expected)

    def test_text_node_bold(self):
        tn = TextNode("Bold", TextType.BOLD)
        expected = LeafNode("b", "Bold")
        self.assertEqual(text_node_to_html_node(tn), expected)

    def test_text_node_italic(self):
        tn = TextNode("Italic", TextType.ITALIC)
        expected = LeafNode("i", "Italic")
        self.assertEqual(text_node_to_html_node(tn), expected)

    def test_text_node_code(self):
        tn = TextNode("print('hello')", TextType.CODE)
        expected = LeafNode("code", "print('hello')")
        self.assertEqual(text_node_to_html_node(tn), expected)

    def test_text_node_link(self):
        tn = TextNode("Click me", TextType.LINK, url="https://example.com")
        expected = LeafNode("a", "Click me", props={
                            "href": "https://example.com"})
        self.assertEqual(text_node_to_html_node(tn), expected)

    def test_text_node_image(self):
        tn = TextNode("An image", TextType.IMAGE,
                      url="https://img.com/cat.png")
        expected = LeafNode(
            "img", "", props={"src": "https://img.com/cat.png", "alt": "An image"})
        self.assertEqual(text_node_to_html_node(tn), expected)

    def test_text_node_invalid_type(self):
        class FakeType:
            pass
        tn = TextNode("oops", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(tn)


if __name__ == "__main__":
    unittest.main()

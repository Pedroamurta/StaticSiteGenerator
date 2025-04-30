import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_df_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a not text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_df_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_df_url(self):
        node1 = TextNode("text", TextType.LINK, url="http://a.com")
        node2 = TextNode("text", TextType.LINK, url="http://b.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("Click here", TextType.LINK, "http://example.com")
        self.assertEqual(repr(node), "TextNode(Click here, link, http://example.com)")




if __name__ == "__main__":
    unittest.main()

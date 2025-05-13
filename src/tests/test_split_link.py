import unittest
from nodes.textnode import TextNode, TextType
from utils.split_nodes_link import split_nodes_link


class TestSplitNodesLink(unittest.TestCase):

    def test_no_links(self):
        input_nodes = [TextNode("Just some text", TextType.TEXT)]
        expected = [TextNode("Just some text", TextType.TEXT)]
        self.assertEqual(split_nodes_link(input_nodes), expected)

    def test_single_link_in_middle(self):
        input_nodes = [
            TextNode("Before [Google](https://google.com) after", TextType.TEXT)]
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" after", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link(input_nodes), expected)

    def test_link_at_start(self):
        input_nodes = [TextNode("[Start](start.com) then text", TextType.TEXT)]
        expected = [
            TextNode("Start", TextType.LINK, "start.com"),
            TextNode(" then text", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link(input_nodes), expected)

    def test_link_at_end(self):
        input_nodes = [TextNode("Click this [link](end.com)", TextType.TEXT)]
        expected = [
            TextNode("Click this ", TextType.TEXT),
            TextNode("link", TextType.LINK, "end.com")
        ]
        self.assertEqual(split_nodes_link(input_nodes), expected)

    def test_only_link(self):
        input_nodes = [TextNode("[JustLink](link.com)", TextType.TEXT)]
        expected = [TextNode("JustLink", TextType.LINK, "link.com")]
        self.assertEqual(split_nodes_link(input_nodes), expected)

    def test_multiple_links(self):
        input_nodes = [
            TextNode("[One](1.com) middle [Two](2.com) end", TextType.TEXT)
        ]
        expected = [
            TextNode("One", TextType.LINK, "1.com"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("Two", TextType.LINK, "2.com"),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link(input_nodes), expected)

    def test_non_text_nodes_are_untouched(self):
        input_nodes = [TextNode("Ignore me", TextType.CODE)]
        expected = [TextNode("Ignore me", TextType.CODE)]
        self.assertEqual(split_nodes_link(input_nodes), expected)

    def test_link_with_empty_text(self):
        input_nodes = [TextNode("Start [](/blank) end", TextType.TEXT)]
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("", TextType.LINK, "/blank"),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link(input_nodes), expected)

    def test_link_with_empty_url(self):
        input_nodes = [TextNode("Check [here]()", TextType.TEXT)]
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("here", TextType.LINK, "")
        ]
        self.assertEqual(split_nodes_link(input_nodes), expected)


if __name__ == "__main__":
    unittest.main()

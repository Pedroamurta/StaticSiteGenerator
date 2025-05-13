import unittest
from nodes.textnode import TextNode, TextType
from utils.split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_simple_bold_split(self):
        input_nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold_segments(self):
        input_nodes = [
            TextNode("**Bold1** middle **Bold2** end", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("Bold1", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("Bold2", TextType.BOLD),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_non_text_node_passthrough(self):
        input_nodes = [TextNode("some code", TextType.CODE)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("some code", TextType.CODE)])

    def test_invalid_syntax_raises(self):
        input_nodes = [TextNode("Unmatched **bold here", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        self.assertIn("Invalid markdown syntax", str(context.exception))

    def test_no_delimiters(self):
        input_nodes = [TextNode("Just plain text", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("Just plain text", TextType.TEXT)])

    def test_empty_input(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_multiple_in_a_row(self):
        input_nodes = [TextNode("a**b**c**d**e", TextType.TEXT)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("a", TextType.TEXT), 
                                  TextNode("b", TextType.BOLD), 
                                  TextNode("c", TextType.TEXT),
                                  TextNode("d", TextType.BOLD),
                                  TextNode("e", TextType.TEXT)])


if __name__ == "__main__":
    unittest.main()

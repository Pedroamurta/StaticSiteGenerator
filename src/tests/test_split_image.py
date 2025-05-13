import unittest
from nodes.textnode import TextNode, TextType
from utils.split_nodes_image import split_nodes_image


class TestSplitNodesImage(unittest.TestCase):

    def test_no_images(self):
        input_nodes = [TextNode("Just plain text", TextType.TEXT)]
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(split_nodes_image(input_nodes), expected)

    def test_single_image_in_middle(self):
        input_nodes = [TextNode("Before ![cat](cat.png) after", TextType.TEXT)]
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(input_nodes), expected)

    def test_image_at_start(self):
        input_nodes = [TextNode("![logo](logo.png) then intro", TextType.TEXT)]
        expected = [
            TextNode("logo", TextType.IMAGE, "logo.png"),
            TextNode(" then intro", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(input_nodes), expected)

    def test_image_at_end(self):
        input_nodes = [
            TextNode("Header then ![footer](foot.png)", TextType.TEXT)]
        expected = [
            TextNode("Header then ", TextType.TEXT),
            TextNode("footer", TextType.IMAGE, "foot.png"),
        ]
        self.assertEqual(split_nodes_image(input_nodes), expected)

    def test_only_image(self):
        input_nodes = [TextNode("![solo](img.png)", TextType.TEXT)]
        expected = [TextNode("solo", TextType.IMAGE, "img.png")]
        self.assertEqual(split_nodes_image(input_nodes), expected)

    def test_multiple_images(self):
        input_nodes = [
            TextNode("![one](1.png) middle ![two](2.jpg) end", TextType.TEXT)
        ]
        expected = [
            TextNode("one", TextType.IMAGE, "1.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "2.jpg"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(input_nodes), expected)

    def test_non_text_nodes_are_untouched(self):
        input_nodes = [TextNode("Not an image", TextType.BOLD)]
        expected = [TextNode("Not an image", TextType.BOLD)]
        self.assertEqual(split_nodes_image(input_nodes), expected)

    def test_image_with_empty_alt_text(self):
        input_nodes = [
            TextNode("Text before ![](img.png) text after", TextType.TEXT)]
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "img.png"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(input_nodes), expected)


if __name__ == "__main__":
    unittest.main()

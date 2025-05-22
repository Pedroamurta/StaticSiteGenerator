import unittest
from utils.inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
)

from nodes.textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):

    # -----------------
    # nodes delimeter
    # -----------------   

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

    # -----------------
    # split_nodes_image
    # -----------------

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


    # -----------------
    # split_nodes_link
    # -----------------

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


    # -----------------
    # text_to_textnode
    # -----------------

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


    # ----------------------
    # extract_markdown_links
    # ----------------------

    def test_single_link(self):
        text = "Visit [OpenAI](https://openai.com)"
        expected = [("OpenAI", "https://openai.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "Docs [Python](https://python.org) and [GitHub](https://github.com)"
        expected = [
            ("Python", "https://python.org"),
            ("GitHub", "https://github.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_spaces_in_text(self):
        text = "Search [Google Search](https://google.com)"
        expected = [("Google Search", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_link_text(self):
        text = "[](/empty-text)"
        expected = [("", "/empty-text")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_url(self):
        text = "[no-url]()"
        expected = [("no-url", "")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "Just some regular text."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_malformed_missing_parens(self):
        text = "[oops]this-shouldnt-match"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_nested_brackets(self):
        text = "[Click [here]](https://example.com)"
        # Regex matches the inner-most closing ]
        expected = [("Click [here]", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_ignores_images(self):
        text = "Image: ![alt](img.png) and a [link](url.com)"
        expected = [("link", "url.com")]
        self.assertEqual(extract_markdown_links(text), expected)


    # ------------------------
    # extract_markdown_images
    # ------------------------

    def test_single_image(self):
        text = "This is an image: ![cat](https://example.com/cat.jpg)"
        expected = [("cat", "https://example.com/cat.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "![dog](url1) some text ![bird](url2)"
        expected = [("dog", "url1"), ("bird", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_at_start_and_end(self):
        text = "![start](s.png) in the middle ![end](e.png)"
        expected = [("start", "s.png"), ("end", "e.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_empty_alt_text(self):
        text = "![](empty.png)"
        expected = [("", "empty.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_empty_url(self):
        text = "![no-url]()"
        expected = [("no-url", "")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_malformed_image_missing_parenthesis(self):
        text = "![alt text]image.jpg"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_malformed_image_missing_brackets(self):
        text = "!alt text](image.jpg)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_text_with_no_images(self):
        text = "This is just some text with no images at all."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_nested_brackets_in_alt_text(self):
        text = "![click [here]](url.png)"
        expected = [("click [here]", "url.png")]
        self.assertEqual(extract_markdown_images(text), expected)


if __name__ == "__main__":
    unittest.main()

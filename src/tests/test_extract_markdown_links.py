import unittest
from utils.extract_links import extract_markdown_links


class TestExtractMarkdownLinks(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()

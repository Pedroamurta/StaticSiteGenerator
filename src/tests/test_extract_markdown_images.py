import unittest
from utils.extract_images import extract_markdown_images


class TestExtractMarkdownImages(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()

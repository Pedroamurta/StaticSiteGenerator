import unittest
from utils.markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_single_block(self):
        text = "This is a single paragraph."
        expected = ["This is a single paragraph."]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_two_paragraphs(self):
        text = "First paragraph.\n\nSecond paragraph."
        expected = ["First paragraph.", "Second paragraph."]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_trailing_newlines(self):
        text = "\n\nFirst paragraph.\n\nSecond.\n\n\n"
        expected = ["First paragraph.", "Second."]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_blocks_with_internal_newlines(self):
        text = "Header\nLine 2\n\nAnother block\nLine B"
        expected = ["Header\nLine 2", "Another block\nLine B"]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_only_whitespace(self):
        text = "    \n   \n\n   "
        expected = [""]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_empty_string(self):
        text = ""
        expected = [""]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_multiple_consecutive_blocks(self):
        text = "A\n\nB\n\nC"
        expected = ["A", "B", "C"]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == '__main__':
    unittest.main()

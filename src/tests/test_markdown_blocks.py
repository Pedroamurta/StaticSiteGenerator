import unittest
from utils.markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


class TestMarkdownToHTML(unittest.TestCase):

    # ------------------
    # markdown_to_blocks
    # ------------------

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


    # ------------------
    # block_to_blocktype
    # ------------------

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type(
            "###### Level 6 Heading"), BlockType.HEADING)

    def test_code(self):
        block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote\n> Another line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is just a normal block of text with no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_unordered_list_fails(self):
        block = "- Item 1\nItem 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_ordered_list(self):
        block = "1. One\n3. Skipped Two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()

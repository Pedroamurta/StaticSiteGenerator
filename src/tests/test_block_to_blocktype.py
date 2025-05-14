import unittest
from utils.block_to_block_type import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):

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

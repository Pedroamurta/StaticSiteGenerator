import re
from enum import Enum
from nodes.htmlnode import HTMLnode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def markdown_to_blocks(markdown):
    return markdown.strip().split("\n\n")


def block_to_block_type(block):
    lines = block.splitlines()

    if lines[0].startswith("```") and lines[-1].startswith("```") and len(lines) >= 2:
        return BlockType.CODE

    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    ordered = True
    for idx, line in enumerate(lines):
        if not re.match(rf"^{idx+1}\. ", line):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html(markdown):
    
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        pass
   

def block_to_html(block):
    block_type = block_to_block_type(block)

 
            
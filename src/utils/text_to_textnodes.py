from nodes.textnode import TextNode, TextType
from utils.split_nodes_image import split_nodes_image
from utils.split_nodes_link import split_nodes_link
from utils.split_nodes_delimiter import split_nodes_delimiter

def text_to_textnodes(text):

    nodes = split_nodes_image([TextNode(text, TextType.TEXT)])

    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes
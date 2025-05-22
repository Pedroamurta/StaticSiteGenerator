import re
from nodes.textnode import TextNode, TextType



def text_to_textnodes(text):
    nodes = split_nodes_image([TextNode(text, TextType.TEXT)])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    all_new_nodes = []
    for old_node in old_nodes:
        new_node = []

        if old_node.text_type != TextType.TEXT or delimiter not in old_node.text:
            all_new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown syntax")

        for i in range(len(parts)):

            if i % 2 == 1:
                new_node.append(TextNode(parts[i], text_type))
            else:
                new_node.append(TextNode(parts[i], TextType.TEXT))

        all_new_nodes.extend(new_node)

    return all_new_nodes


def split_nodes_image(old_nodes):
    all_new_nodes = []

    for old_node in old_nodes:
        new_nodes = []

        if old_node.text_type != TextType.TEXT:
            all_new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        if not images:
            all_new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for image_alt_text, image_url in images:
            image_markdown = f"![{image_alt_text}]({image_url})"

            parts = remaining_text.split(image_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(
                TextNode(image_alt_text, TextType.IMAGE, image_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

        all_new_nodes.extend(new_nodes)

    return all_new_nodes


def split_nodes_link(old_nodes):
    all_new_nodes = []

    for old_node in old_nodes:
        new_nodes = []

        if old_node.text_type != TextType.TEXT:
            all_new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if not links:
            all_new_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"

            parts = remaining_text.split(link_markdown, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

        all_new_nodes.extend(new_nodes)

    return all_new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

from nodes.textnode import TextNode, TextType
from utils.extract_links import extract_markdown_links


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

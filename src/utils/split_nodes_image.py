from nodes.textnode import TextNode, TextType
from utils.extract_images import extract_markdown_images

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

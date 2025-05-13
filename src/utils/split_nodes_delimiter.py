from nodes.textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    all_new_nodes = []
    for old_node in old_nodes:
        new_node = []

        if  old_node.text_type != TextType.TEXT or delimiter not in old_node.text:
            all_new_nodes.append(old_node)
            continue
        
        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown syntax")
            
        for i in range(len(parts)):

            if i % 2 ==  1:
                new_node.append(TextNode(parts[i], text_type))
            else:
                new_node.append(TextNode(parts[i], TextType.TEXT))
        
        all_new_nodes.extend(new_node)
    
    return all_new_nodes

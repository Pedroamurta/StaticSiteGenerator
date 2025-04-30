from htmlnode import HTMLnode

class LeafNode(HTMLnode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode Object must have value attribute")
        
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.format_props_for_tag()}>{self.value}</{self.tag}>"

        
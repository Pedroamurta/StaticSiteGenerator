from htmlnode import HTMLnode

class LeafNode(HTMLnode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode Object must have value attribute")
        
        if not self.tag:
            return self.value

        props_to_add = ""
        if self.props:
            props_to_add = " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

        return f"<{self.tag}{props_to_add}>{self.value}</{self.tag}>"

        
from htmlnode import HTMLnode

class LeafNode(HTMLnode):

    SELF_CLOSING_TAGS = {"img", "br", "hr", "meta", "input", "link"}

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

        
    
    def to_html(self):
        

        if not self.value and self.tag not in self.SELF_CLOSING_TAGS:
            raise ValueError("LeafNode Object must have value attribute")

        if not self.tag:
            return self.value

        if self.tag in self.SELF_CLOSING_TAGS:
            return f"<{self.tag}{self.format_props_for_tag()} />"

        return f"<{self.tag}{self.format_props_for_tag()}>{self.value}</{self.tag}>"
        
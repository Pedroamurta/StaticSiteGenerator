from htmlnode import HTMLnode

class ParentNode(HTMLnode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode Object must have a tag")
        if not self.children:
            raise ValueError("ParentNode Object must have children")
        
        html = f"<{self.tag}{self.format_props_for_tag()}>"

        for child in self.children:
            html += child.to_html()
        
        html += f"</{self.tag}>"

        return html
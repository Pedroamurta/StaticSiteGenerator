class HTMLnode():

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLnode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def format_props_for_tag(self):
        formated_props = ""
        if self.props:
            formated_props = " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
        
        return formated_props

    def props_to_html(self):
        html = ""

        if self.props:
            for key in self.props:
                html += f"{key}: {self.props[key]}"
            
        return html
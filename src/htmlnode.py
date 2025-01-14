from functools import reduce

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return "" 
        return reduce(lambda x, y: x + f' {y[0]}="{y[1]}"', self.props.items(), "")
       
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("The LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("The ParentNode must have a tag")
        if self.children is None:
            raise ValueError("The ParentNode must have children")
        return f"<{self.tag}{self.props_to_html()}>" + self.recursive_children_html(self.children) + f"</{self.tag}>"

    def recursive_children_html(self , children_list):
        if len(children_list) == 0:
            return "" 
        return f"{children_list[0].to_html()}" + f"{self.recursive_children_html(children_list[1:])}"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
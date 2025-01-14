import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_exception(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
            "other": "ham",
            "fruit": "banana",
        }
        node = HTMLNode(props = props)
        expected_output =  ' href="https://www.google.com" target="_blank" other="ham" fruit="banana"'
        self.assertEqual(expected_output, node.props_to_html())

    def test_props_none_to_html(self):
        node = HTMLNode()
        expected_output = ""
        self.assertEqual(expected_output, node.props_to_html())

    def test_repr(self):
        node = HTMLNode(tag = "p", value = "I like big fruits", children = [HTMLNode(), HTMLNode()], props = {"href": "www.google.com", "target": "you"})
        expected_output = "HTMLNode(p, I like big fruits, [HTMLNode(None, None, None, None), HTMLNode(None, None, None, None)], {'href': 'www.google.com', 'target': 'you'})"
        self.assertEqual(repr(node), expected_output)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        # No props
        node_no_props = LeafNode("p", "This is a paragraph of text.")
        expected_no_props = "<p>This is a paragraph of text.</p>"
        self.assertEqual(expected_no_props, node_no_props.to_html())
        # With props
        node_props = LeafNode("a", "Click me!", props = {"href": "https://www.google.com"})
        expected_props = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node_props.to_html(), expected_props)
        # None value
        node_none_value = LeafNode("p", None)
        self.assertRaises(ValueError, node_none_value.to_html)
        # None tag
        node_none_tag = LeafNode(None, "This is some text, baby.")
        expected_none_tag = "This is some text, baby."
        self.assertEqual(expected_none_tag, node_none_tag.to_html())

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        # Node with tag and children
        node_tag_children = ParentNode(
        "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ],
        )
        expecteded_tag_children = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(expecteded_tag_children, node_tag_children.to_html())
        # Node with None tag
        node_none_tag = ParentNode(None, [LeafNode("b", "Bold text"), LeafNode("a", "Hello world")])
        self.assertRaises(ValueError, node_none_tag.to_html)
        # Node with None children
        node_none_children = ParentNode("p", None)
        self.assertRaises(ValueError, node_none_children.to_html)
        # Node with tag, children and props
        node_tag_children_props = ParentNode(
        "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ], {"href": "https://www.youtube.com", "target": "you", "level": "69"}
        )
        expected_tag_children_props = "<p href=\"https://www.youtube.com\" target=\"you\" level=\"69\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(expected_tag_children_props, node_tag_children_props.to_html())
        # Empty list
        node_empty_list = ParentNode("p", [])
        expected_empty_list = "<p></p>"
        self.assertEqual(node_empty_list.to_html(), expected_empty_list)
        # Nested parents
        node_nested_parents = ParentNode("p", [node_tag_children, LeafNode("b", "you are bold")])
        expected_nested_parents = "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>you are bold</b></p>"
        self.assertEqual(node_nested_parents.to_html(), expected_nested_parents)

if __name__ == "__main__":
    unittest.main()
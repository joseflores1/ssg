import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_ineq_text(self):
        # DIfferent text
        node = TextNode("This is a test node", TextType.BOLD_TEXT)
        node2 = TextNode("This is text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_ineq_TextType(self):
        # Different TextType
        node = TextNode("This is text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)
    
    def test_ineq_urls(self):
        node = TextNode("This is text node", TextType.BOLD_TEXT, "www.google.com")
        node2 = TextNode("This is text node", TextType.BOLD_TEXT, "www.youtube.com")
        self.assertNotEqual(node, node2)
        

    def test_none_url(self):
        node = TextNode("This is a test node", TextType.IMAGE)
        self.assertIsNone(node.url)
    
    def test_repr(self):
        node = str(TextNode("Texting with dialog", TextType.LINK))
        expected_string = "TextNode(Texting with dialog, LINK, None)"
        self.assertEqual(node, expected_string)

    def test_text_node_to_leaf_node(self):
        # TextType.TEXT
        text_node = TextNode("This is a text node", TextType.NORMAL_TEXT)    
        self.assertEqual(text_node_to_html_node(text_node), LeafNode(None, "This is a text node"))
        # TextType.BOLD
        bold_node = TextNode("This is a bold node", TextType.BOLD_TEXT)
        self.assertEqual(text_node_to_html_node(bold_node), LeafNode("b", "This is a bold node"))
        # TextType.ITALIC
        italic_node = TextNode("This is an italic node", TextType.ITALIC_TEXT)
        self.assertEqual(text_node_to_html_node(italic_node), LeafNode("i", "This is an italic node"))
        # TextType.CODE
        code_node = TextNode("This is a code node", TextType.CODE_TEXT)
        self.assertEqual(text_node_to_html_node(code_node), LeafNode("code", "This is a code node"))
        # TextType.LINK
        link_node = TextNode("This is a link node", TextType.LINK, url = "https://www.google.com")
        self.assertEqual(text_node_to_html_node(link_node), LeafNode("a", "This is a link node", props = {"href": "https://www.google.com"}))
        # TextType.IMAGE
        image_node = TextNode("This is an image", TextType.IMAGE, url = "https://www.imgur.com")
        self.assertEqual(text_node_to_html_node(image_node), LeafNode("img", "", {"src": "https://www.imgur.com", "alt": "This is an image"}))

if __name__ == "__main__":
    unittest.main()
import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delimiter(self):
        delimeter_tuples = [("`", TextType.CODE_TEXT), ("**", TextType.BOLD_TEXT), ("*", TextType.ITALIC_TEXT)]
        # Only code node list
        code_nodes = [TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT),
                       TextNode("This is such a simple `code` question, you just need to `print(foo) if a == 0`", TextType.NORMAL_TEXT)
                      ]
        expected_code_node =  [
            TextNode("This is text with a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.NORMAL_TEXT),
            TextNode("This is such a simple ", TextType.NORMAL_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" question, you just need to ", TextType.NORMAL_TEXT),
            TextNode("print(foo) if a == 0", TextType.CODE_TEXT)
            ]
        self.assertEqual(split_nodes_delimiter(code_nodes, "`", TextType.CODE_TEXT), expected_code_node)
        # empty node list
        empty_node = []
        expected_empty_node = []
        self.assertEqual(split_nodes_delimiter(empty_node, "**", TextType.BOLD_TEXT), expected_empty_node)
        # multi delimiter node
        multi_del_node = [TextNode("This **is** text **with a lot** *of* `code block` word", TextType.NORMAL_TEXT)]
        expected_multi_del_node = [
            TextNode("This ", TextType.NORMAL_TEXT),
            TextNode("is", TextType.BOLD_TEXT),
            TextNode(" text ", TextType.NORMAL_TEXT),
            TextNode("with a lot", TextType.BOLD_TEXT),
            TextNode(" ", TextType.NORMAL_TEXT),
            TextNode("of", TextType.ITALIC_TEXT),
            TextNode(" ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" word", TextType.NORMAL_TEXT),
        ]
        for delimeter, text_type in delimeter_tuples:
            multi_del_node = split_nodes_delimiter(multi_del_node, delimeter, text_type)
        self.assertEqual(multi_del_node, expected_multi_del_node)
        # Not closed delimiter
        not_closed_node = [TextNode(" *hola", TextType.NORMAL_TEXT)]
        expected_exception = "Invalid markdown, formatted section not closed"
        try:
            split_nodes_delimiter(not_closed_node, "*", TextType.ITALIC_TEXT)
        except Exception as e:
            self.assertEqual(expected_exception, str(e))

if __name__ == "__main__":
    unittest.main()
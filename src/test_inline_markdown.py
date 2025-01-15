import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

    def test_extract_images(self):
        # Normal image text
        normal_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_normal_text = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(normal_text), expected_normal_text)
        # No pattern found
        no_pattern_text = "This is a text iwth a ! rick roll https://i.imgur.com/aKaOqIh.gif"
        expected_no_pattern = []
        self.assertEqual(extract_markdown_images(no_pattern_text), expected_no_pattern)
        # Square brackets within square brackets and parenthesis within parenthesis
        square_nested_text = "This is text with a ![rick roll [super rickroll]](https://i.imgur.com/aKaOqIh.gif (you get me)) and ![obi wan []](https://i.imgur.com/fJRm4Vk.jpeg ())"
        expected_nested_text = []
        self.assertEqual(expected_nested_text, extract_markdown_images(square_nested_text))
        # Link syntax
        link_text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_link_text = []
        self.assertEqual(expected_link_text, extract_markdown_images(link_text))
    
    def test_extract_links(self):
        normal_text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_normal_text = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_links(normal_text), expected_normal_text)
        # No pattern found
        no_pattern_text = "This is a text iwth a  rick roll https://i.imgur.com/aKaOqIh.gif"
        expected_no_pattern = []
        self.assertEqual(extract_markdown_links(no_pattern_text), expected_no_pattern)
        # Square brackets within square brackets and parenthesis within parenthesis
        square_nested_text = "This is text with a [rick roll [super rickroll]](https://i.imgur.com/aKaOqIh.gif (you get me)) and [obi wan []](https://i.imgur.com/fJRm4Vk.jpeg ())"
        expected_nested_text = []
        self.assertEqual(expected_nested_text, extract_markdown_links(square_nested_text))
        # Link syntax
        link_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_link_text = []
        self.assertEqual(expected_link_text, extract_markdown_links(link_text))
    
    def test_separate_links_images(self):
        # Single Link node
        link_node = [TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT
        )]
        expected_node = [
                 TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                 TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                 TextNode(" and ", TextType.NORMAL_TEXT),
                 TextNode(
                     "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                 ),
             ]
        self.assertEqual(split_nodes_link(link_node), expected_node)
        # Single Image Node
        image_node = [TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT
        )]
        expected_node = [
                 TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                 TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                 TextNode(" and ", TextType.NORMAL_TEXT),
                 TextNode(
                     "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                 ),
             ]
        self.assertEqual(split_nodes_image(image_node), expected_node)
        # Image and Link
        image_link_node = [TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT
        )]
        expected_node = [
                 TextNode("This is text with a link ", TextType.NORMAL_TEXT),
                 TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                 TextNode(" and ", TextType.NORMAL_TEXT),
                 TextNode(
                     "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                 ),
             ]
        #first image and then link splitting
        self.assertEqual(split_nodes_link(split_nodes_image(image_link_node)), expected_node)
        # first link and then image splitting
        self.assertEqual(split_nodes_image(split_nodes_link(image_link_node)), expected_node)
        # Empty list
        empty_list = []
        expected_output = []
        self.assertEqual(split_nodes_image(empty_list), expected_output)
        self.assertEqual(split_nodes_link(empty_list), expected_output)
        # No found image or link delimiter
        no_img_link_list = [TextNode("This is a text without a 'valid' delimiter", TextType.NORMAL_TEXT)]
        expected_output = [TextNode("This is a text without a 'valid' delimiter", TextType.NORMAL_TEXT)]
        self.assertEqual(split_nodes_image(no_img_link_list), expected_output)

    def test_split_image_single(self):
            node = TextNode(
                "![image](https://www.example.COM/IMAGE.PNG)",
                TextType.NORMAL_TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
                ],
                new_nodes,
            )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_text = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.NORMAL_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected_text)
        # Empty text
        text = ""
        expected_output = []
        self.assertEqual(text_to_textnodes(text), expected_output)
        # No delimiter or links/images
        text = "Dígase que la esencia del ser proviene de la voluntad, ley y amor de Dios. De esta manera, el pensar refleja la susodicha (no sé qué estoy escribiendo)"
        expected_output = [TextNode("Dígase que la esencia del ser proviene de la voluntad, ley y amor de Dios. De esta manera, el pensar refleja la susodicha (no sé qué estoy escribiendo)", TextType.NORMAL_TEXT)]
        self.assertEqual(text_to_textnodes(text), expected_output)

if __name__ == "__main__":
    unittest.main()
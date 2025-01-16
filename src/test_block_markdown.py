import unittest
from block_markdown import markdown_to_blocks, block_to_block_type


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type_headings(self):
        # One level heading
        markdown = """
# This is a heading
"""
        expected_output = "heading"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # Two level heading
        markdown = """
## This is a heading
"""
        expected_output = "heading"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # Three level heading
        markdown = """
### This is a heading
"""
        expected_output = "heading"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # Four level heading
        markdown = """
#### This is a heading
"""
        expected_output = "heading"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # Five level heading
        markdown = """
##### This is a heading
"""
        expected_output = "heading"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # Six level heading
        markdown = """
###### This is a heading
"""
        expected_output = "heading"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # No space heading
        markdown = """
######This is a heading
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # No heading
        markdown = """
This is a heading
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)


    def test_block_to_block_type_code(self):
        # Normal code
        markdown = """
```
This is a heading
```
"""
        expected_output = "code"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # Not closed code
        markdown = """
```
This is a heading
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # No code
        markdown = """

This is a heading
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)


    def test_block_to_block_type_quote(self):
        # Normal quotes
        markdown = """
> This is a quote
> Followed by another quote line
> And a third
> And another one
> Another one
"""
        expected_output = "quote"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # No > symbol in everyline
        markdown = """
> This is a quote
Followed by another quote line
And a third
> And another one
> Another one
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)


    def test_block_to_block_type_ul(self):
        # Normal * list
        markdown = """
* This is a quote
* Followed by another quote line
* And a third
* And another one
* Another one
"""
        expected_output = "unordered_list"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # Mix * and - list
        markdown = """
* This is a quote
- Followed by another quote line
- And a third
* And another one
* Another one
"""
        expected_output = "unordered_list"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # Only - list
        markdown = """
- This is a quote
- Followed by another quote line
- And a third
- And another one
- Another one
"""
        expected_output = "unordered_list"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # No space list
        markdown = """
* This is a quote
- Followed by another quote line
- And a third
* And another one
*Another one
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # No list
        markdown = """
This is a quote
Followed by another quote line
> And a third
And another one
Another one
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)


    def test_block_to_block_type_ol(self):
        # Normal ordered list
        markdown = """
1. This is a quote
2. Followed by another quote line
3. And a third
4. And another one
5. Another one
"""
        expected_output = "ordered_list"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # No valid list
        markdown = """
0. First item
1. This is a quote
2. Followed by another quote line
3. And a third
4. And another one
5. Another one
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # No space list
        markdown = """
1.This is a quote
2. Followed by another quote line
3. And a third
4. And another one
5. Another one
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)

        # No pojnt list
        markdown = """
1 This is a quote
2 Followed by another quote line
3 And a third
4 And another one
5 Another one
"""
        expected_output = "paragraph"
        self.assertEqual(block_to_block_type(markdown), expected_output)


if __name__ == "__main__":
    unittest.main()
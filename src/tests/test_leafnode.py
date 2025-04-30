import unittest
from nodes.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click!", {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Click!</a>')
    
    def test_leaf_tag_missing_error(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leafnode_self_closing_img_with_props(self):
        node = LeafNode("img", "", props={"src": "cat.png", "alt": "A cat"})
        self.assertEqual(node.to_html(), '<img src="cat.png" alt="A cat" />')


    def test_leafnode_self_closing_br_no_props(self):
        node = LeafNode("br", "")
        self.assertEqual(node.to_html(), "<br />")


    def test_leafnode_normal_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leafnode_self_closing_hr_with_props(self):
        node = LeafNode("hr", "", props={"class": "line"})
        self.assertEqual(node.to_html(), '<hr class="line" />')


    def test_leafnode_self_closing_ignores_value(self):
        node = LeafNode("img", "ignored", props={"src": "x.png"})
        self.assertEqual(node.to_html(), '<img src="x.png" />')

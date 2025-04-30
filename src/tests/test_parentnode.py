import unittest
from nodes.parentnode import ParentNode
from nodes.leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
    
    def test_to_html_multiple_children(self):
        child1 = LeafNode("p", "first")
        child2 = LeafNode("p", "second")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><p>first</p><p>second</p></div>")

    def test_to_html_parent_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "container"})
        self.assertEqual(parent.to_html(),'<div class="container"><span>child</span></div>')
    
    def test_to_html_mixed_children(self):
        leaf = LeafNode("p", "text")
        nested = ParentNode("section", [LeafNode("b", "bold")])
        parent = ParentNode("div", [leaf, nested])
        self.assertEqual(
            parent.to_html(),
            "<div><p>text</p><section><b>bold</b></section></div>",
        )

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_to_html_parent_no_tag(self):
        child = LeafNode("span", "hello")
        with self.assertRaises(ValueError):
            ParentNode(None, [child]).to_html()

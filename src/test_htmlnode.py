import unittest

from htmlnode import HTMLnode

class TestHTMLNode(unittest.TestCase):

    def test_initialization_all_args(self):
        node = HTMLnode("p", "Hello", ["child1"], {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, ["child1"])
        self.assertEqual(node.props, {"class": "text"})
    
    def test_initialization_defaults(self):
        node = HTMLnode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        node = HTMLnode(tag="div", value="Hello", props={"style": "color:red;"})
        expected = "HTMLnode(tag: div, value: Hello, children: None, props: {'style': 'color:red;'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_with_props(self):
        node = HTMLnode(props={"class": "header", "id": "main"})
        html = node.props_to_html()
        self.assertIn("class: header", html)
        self.assertIn("id: main", html)

    def test_props_to_html_no_props(self):
        node = HTMLnode()
        self.assertEqual(node.props_to_html(), "")
    

    def test_to_html_raises_error(self):
        node = HTMLnode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
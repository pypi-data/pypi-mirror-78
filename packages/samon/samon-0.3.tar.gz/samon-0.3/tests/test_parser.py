from io import BytesIO
from unittest import TestCase

from doculabs.samon import registry
from doculabs.samon.elements import BaseElement, AnonymusElement
from doculabs.samon.environment import Environment
from doculabs.samon.parser import Parser
from doculabs.samon.template import Template


class ParserTest(TestCase):
    def test_parse_result(self):
        parser = Parser(environment=Environment(loader=None))
        template = parser.parse(b'<root></root>', template_name='test')
        self.assertIsInstance(template, Template)
        self.assertIsInstance(template.root_element, BaseElement)

    def test_parse_tree(self):
        tmpl = b"""
        <root>
            <child1>
                <subchild></subchild>
            </child1>
            <child2>
                <subchild></subchild>
                <subchildd></subchildd>
            </child2>
        </root>
        """
        parser = Parser(environment=Environment(loader=None))
        template = parser.parse(tmpl, template_name='test')

        root = template.root_element
        self.assertIsInstance(root, BaseElement)
        self.assertEqual(root.parent, None)
        self.assertEqual(len(root.children), 2)
        self.assertEqual(root.children[0].xml_tag, 'child1')
        self.assertEqual(root.children[1].xml_tag, 'child2')
        self.assertEqual(len(root.children[0].children), 1)
        self.assertEqual(len(root.children[1].children), 2)
        # template.show_element_tree()

    def test_parse_attributes(self):
        tmpl = b"""
        <root xmlns:c="http://example.org">
            <child attr1="val1" c:attr2="val2" />
            <child2></child2>
        </root>
        """
        parser = Parser(environment=Environment(loader=None))
        template = parser.parse(tmpl, template_name='test')

        child1 = template.root_element.children[0]
        self.assertSequenceEqual(list(child1.xml_attrs.keys()), ['attr1', '{http://example.org}attr2'])
        self.assertSequenceEqual(list(child1.xml_attrs.values()), ['val1', 'val2'])

        child2 = template.root_element.children[1]
        self.assertEqual(child2.xml_attrs, {})

    def test_parse_custom_element(self):
        tmpl = b"""
        <root>
            <example attr1="1" attr2="sdf" />
        </root>
        """

        @registry.element('example')
        class Example(BaseElement):
            pass

        parser = Parser(environment=Environment(loader=None))
        template = parser.parse(tmpl, template_name='test')

        self.assertIsInstance(template.root_element, BaseElement)
        self.assertIsInstance(template.root_element.children[0], Example)

    def test_parse_text(self):
        tmpl = b"""
        <root>
            some 
            example text
            <child1>child1</child1>
            exmaple2
            <child2>child2</child2>
        </root>
        """
        parser = Parser(environment=Environment(loader=None))
        template = parser.parse(tmpl, template_name='test')

        root = template.root_element
        self.assertEqual(len(root.children), 5)
        self.assertIsInstance(root.children[0], AnonymusElement)
        self.assertEqual(root.children[0].text, 'some')
        self.assertIsInstance(root.children[1], AnonymusElement)
        self.assertEqual(root.children[1].text, 'example text')
        self.assertIsInstance(root.children[3], AnonymusElement)
        self.assertEqual(root.children[3].text, 'exmaple2')

        self.assertEqual(root.children[2].children[0].text, 'child1')
        self.assertEqual(root.children[4].children[0].text, 'child2')

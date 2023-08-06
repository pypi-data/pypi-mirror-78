from io import StringIO
from pathlib import Path
from unittest import TestCase

from doculabs.samon import constants
from doculabs.samon.elements import BaseElement, AnonymusElement
from doculabs.samon.expressions import Condition, ForLoop, Bind


class BaseElementTest(TestCase):
    def assertXmlEqual(self, generated_xml: str, xml_benchmark: Path):
        xml_benchmark = Path(__file__).parent / xml_benchmark
        with xml_benchmark.open('r', encoding='utf-8') as f:
            xml_benchmark = f.read()

        self.assertEqual(generated_xml, xml_benchmark)

    def test_parse_xml_attributes(self):
        xml_attrs = {  # AttributesNSImpl like object
            (None, 'attr1'): 'val1',  # NS, attr_name
            ('http://example.org', 'attr2'): 'val2'
        }

        element = BaseElement(xml_tag='tag', xml_attrs=xml_attrs)
        self.assertEqual(element.xml_attrs, {'attr1': 'val1', '{http://example.org}attr2': 'val2'})

    def test_parse_expressions(self):
        xml_attrs = {
            (constants.XML_NAMESPACE_FLOW_CONTROL, 'if'): 'val == 7',
            (constants.XML_NAMESPACE_FLOW_CONTROL, 'for'): 'a in val',
            (constants.XML_NAMESPACE_DATA_BINDING, 'attr2'): 'val'
        }

        e = BaseElement(xml_tag='tag', xml_attrs=xml_attrs)
        self.assertIsInstance(e.xml_attrs['{https://doculabs.io/2020/xtmpl#control}if'], Condition)
        self.assertIsInstance(e.xml_attrs['{https://doculabs.io/2020/xtmpl#control}for'], ForLoop)
        self.assertIsInstance(e.xml_attrs['{https://doculabs.io/2020/xtmpl#data-binding}attr2'], Bind)

    def test_data_binding(self):
        xml_attrs = {
            (constants.XML_NAMESPACE_DATA_BINDING, 'attr2'): 'val'
        }

        e = BaseElement(xml_tag='tag', xml_attrs=xml_attrs)
        xml = e.to_string(context={'val': 'example_value'}, indent=0).getvalue()
        self.assertEqual(xml, '<tag attr2="example_value">\n</tag>\n')

    def test_eval_forloop(self):
        xml_attrs = {
            (constants.XML_NAMESPACE_FLOW_CONTROL, 'for'): 'a in val',
            (None, 'class'): 'class_name'
        }

        e = BaseElement(xml_tag='tag', xml_attrs=xml_attrs)
        xml = e.to_string(context={'val': [1, 2, 3]}, indent=0).getvalue()
        self.assertXmlEqual(xml, 'assets/elements/forloop.xml')

    def test_eval_if(self):
        xml_attrs = {
            (constants.XML_NAMESPACE_FLOW_CONTROL, 'if'): 'val == 7',
            (None, 'class'): 'class_name'
        }

        e = BaseElement(xml_tag='tag', xml_attrs=xml_attrs)
        xml = e.to_string(context={'val': 8}, indent=0).getvalue()
        self.assertEqual(xml, '')

        xml = e.to_string(context={'val': 7}, indent=0).getvalue()
        self.assertXmlEqual(xml, 'assets/elements/ifcond.xml')

    def test_if_and_for_precedence(self):
        xml_attrs = {
            (constants.XML_NAMESPACE_FLOW_CONTROL, 'if'): 'val > 7',
            (constants.XML_NAMESPACE_FLOW_CONTROL, 'for'): 'val in val2',
            (constants.XML_NAMESPACE_DATA_BINDING, 'attr1'): 'val',
        }

        e = BaseElement(xml_tag='tag', xml_attrs=xml_attrs)
        xml = e.to_string(context={'val2': [7, 8, 9], 'val': 7}, indent=0).getvalue()
        self.assertXmlEqual(xml, 'assets/elements/if_and_for.xml')

    def test_render_anonymuselement(self):
        e = AnonymusElement(text='example')
        self.assertEqual(e.to_string(context={}).getvalue(), 'example\n')

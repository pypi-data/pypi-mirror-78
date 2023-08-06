from pathlib import Path
from unittest import TestCase

from tests.mock import get_base_environment


class TemplateTest(TestCase):
    def assertXmlEqual(self, generated_xml: str, xml_benchmark: Path):
        xml_benchmark = Path(__file__).parent / xml_benchmark
        with xml_benchmark.open('r', encoding='utf-8') as f:
            xml_benchmark = f.read()

        self.assertEqual(generated_xml, xml_benchmark)

    def test_render(self):
        env = get_base_environment()
        template = env.get_template('template2.xml')
        xml = template.render_to_string(context={'iterable': [1, 2, 3], 'value': 8})
        self.assertXmlEqual(xml, 'assets/base/template2_rendered.xml')

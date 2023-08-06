from pathlib import Path

from unittest import TestCase

from doculabs.samon.template import Template
from doculabs.samon.environment import Environment
from doculabs.samon.loaders import FileSystemLoader
from tests.mock import get_base_environment


class EnvironmentTest(TestCase):
    def test_initialize(self):
        env = Environment(loader=FileSystemLoader('~'))
        self.assertEqual(env.loader.search_path, [Path.home()])

    def test_get_template(self):
        env = get_base_environment()
        template = env.get_template('template1.xml')
        self.assertIsInstance(template, Template)
        self.assertEqual(template.root_element.xml_tag, 'root')

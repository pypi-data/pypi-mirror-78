from pathlib import Path
from unittest import TestCase
from tempfile import TemporaryDirectory

from doculabs.samon.exceptions import TemplateNotFound
from doculabs.samon.loaders import FileSystemLoader


class FileSystemLoaderTest(TestCase):
    def test_init_search_path(self):
        loader = FileSystemLoader(search_path='~/templates')
        self.assertEqual(loader.search_path, [Path.home() / 'templates'])

        loader = FileSystemLoader(search_path=Path('/tmp/'))
        self.assertEqual(loader.search_path, [Path('/tmp')])

        loader = FileSystemLoader(search_path=['/tmp/', Path('/example')])
        self.assertEqual(loader.search_path, [Path('/tmp'), Path('/example')])

    def test_get_source(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir)
            with (p / 'template.xml').open('w', encoding='utf-8') as f:
                f.write('<example></example>')

            loader = FileSystemLoader(search_path=p)
            source = loader.get_source('template.xml')
            self.assertEqual(source, b'<example></example>')

            self.assertRaises(TemplateNotFound, lambda: loader.get_source('example2.xml'))

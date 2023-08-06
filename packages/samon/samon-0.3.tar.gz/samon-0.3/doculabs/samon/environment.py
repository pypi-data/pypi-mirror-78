from copy import copy

from doculabs.samon import registry
from doculabs.samon.loaders import BaseLoader
from doculabs.samon.parser import Parser
from doculabs.samon.template import Template


class Environment:
    DEFAULT_TEMPLATE_CLASS = Template

    def __init__(self, loader: BaseLoader):
        self.loader = loader
        self.registry = copy(registry)
        self.template_class = self.DEFAULT_TEMPLATE_CLASS
        self.parser = Parser(environment=self)

    def get_template(self, template_name):
        src, source_path = self.loader.get_source(template_name)
        template = self.parser.parse(src, template_name=template_name)
        template.source_path = source_path

        return template

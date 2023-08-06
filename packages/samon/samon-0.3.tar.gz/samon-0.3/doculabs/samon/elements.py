from contextlib import contextmanager
from io import StringIO
from typing import List
from xml.sax.xmlreader import AttributesNSImpl

from doculabs.samon import constants
from doculabs.samon.expressions import Bind, Condition, ForLoop, Expression


class BaseElement:
    def __init__(self, xml_tag: str, xml_attrs: AttributesNSImpl):
        self.xml_tag = xml_tag

        self.xml_attrs = self._parse_xml_attrs(xml_attrs)
        self.parent = None
        self.children = []  # type: List[BaseElement]

    def _parse_xml_attrs(self, xml_attrs: AttributesNSImpl):
        attrs = {}
        for (namespace, attr_name), attr_value in xml_attrs.items():
            if namespace is None:
                attrs[attr_name] = attr_value
            else:
                key = '{' + namespace + '}' + attr_name
                if namespace == constants.XML_NAMESPACE_DATA_BINDING:
                    value = Bind(expr=attr_value)
                elif namespace == constants.XML_NAMESPACE_FLOW_CONTROL:
                    if attr_name == 'if':
                        value = Condition(expr=attr_value)
                    elif attr_name == 'for':
                        value = ForLoop(expr=attr_value)
                    else:
                        raise ValueError  # TODO: raise custom error
                else:
                    value = attr_value

                attrs[key] = value

        return attrs

    def add_child(self, element: 'BaseElement'):
        element.parent = self
        self.children.append(element)

    def build_rendering_tree(self, indent=1):
        yield self, indent
        for child in self.children:
            child.build_rendering_tree(indent=indent + 1)

    def format_xml_attrs(self, context) -> str:
        retval = ''
        for k, v in self.xml_attrs.items():
            if k.startswith(f'{{{constants.XML_NAMESPACE_FLOW_CONTROL}}}'):
                continue
            elif k.startswith(f'{{{constants.XML_NAMESPACE_DATA_BINDING}}}'):
                k = k.replace(f'{{{constants.XML_NAMESPACE_DATA_BINDING}}}', '')

                retval += f' {k}="{v.eval(context)}"'
            else:
                retval += f' {k}="{v}"'

        return retval

    @contextmanager
    def frame(self, io, context, indent):
        indent = constants.INDENT * indent
        io.write(f'{indent}<{self.xml_tag}{self.format_xml_attrs(context)}>\n')
        yield
        io.write(f'{indent}</{self.xml_tag}>\n')

    def to_string(self, context, io=None, indent=0):
        io = io or StringIO()

        if for_loop_def := self.xml_attrs.get(f'{{{constants.XML_NAMESPACE_FLOW_CONTROL}}}for', None):  # type: ForLoop
            for counter, loop_var_name, loop_var_val in for_loop_def.eval(context):
                context['loop'] = {'index': counter, 'index0': counter - 1, 'odd': bool(counter % 2 == 1)}
                context[loop_var_name] = loop_var_val

                if_def = self.xml_attrs.get(f'{{{constants.XML_NAMESPACE_FLOW_CONTROL}}}if', None)
                if if_def is None or if_def.eval(context):
                    with self.frame(io, context, indent):
                        for child in self.children:
                            child.to_string(context, io, indent=indent + 1)
        else:
            if_def = self.xml_attrs.get(f'{{{constants.XML_NAMESPACE_FLOW_CONTROL}}}if', None)
            if if_def is None or if_def.eval(context):
                with self.frame(io, context, indent):
                    for child in self.children:
                        child.to_string(context, io, indent=indent+1)

        return io


class AnonymusElement:
    def __init__(self, text):
        self.text = text

    def to_string(self, context, io=None, indent=0):
        io = io or StringIO()

        indent = constants.INDENT * indent
        io.write(f'{indent}{self.text}\n')
        return io

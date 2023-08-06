from unittest import TestCase

from doculabs.samon.registry import registry
from doculabs.samon.elements import BaseElement
from doculabs.samon.exceptions import ElementNameConflict


class RegistryTest(TestCase):
    def test_empty_registry(self):
        """
        If registry haven't any key to the specific XML tag, then use the BaseElement
        """
        class Tag1:
            pass

        self.assertEqual(registry.get_class_by_name('Tag1'), BaseElement)
        registry.element(Tag1)
        self.assertEqual(registry.get_class_by_name('Tag1'), Tag1)

    def test_register_by_decorator(self):
        @registry.element('tag2')
        class Tag2:
            pass

        self.assertEqual(registry.get_class_by_name('tag2'), Tag2)

    def test_register_multiple(self):
        @registry.element('tag3')
        @registry.element('tag4')
        class Tag3:
            pass

        self.assertEqual(registry.get_class_by_name('tag3'), Tag3)
        self.assertEqual(registry.get_class_by_name('tag4'), Tag3)

    def test_register_name_collision(self):
        @registry.element('tag5')
        class Tag5:
            pass

        self.assertRaises(ElementNameConflict, lambda: registry.element('tag5', object.__class__))

    def test_register_with_namespace(self):
        @registry.element('tag6', namespace='https://example.org')
        class Tag6:
            pass

        self.assertEqual(registry.get_class_by_name('tag6'), BaseElement)
        self.assertEqual(registry.get_class_by_name('{https://example.org}tag6'), Tag6)

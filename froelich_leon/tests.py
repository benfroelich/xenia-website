from django.template import Context, Template
from django.test import SimpleTestCase

from .logging import MissingVariableError


class MissingVariableErrorFilterTests(SimpleTestCase):
    def test_missing_variable(self):
        template = Template("Hi {{ name }}", name="index.html")
        context = Context({"nome": "Adam"})

        with self.assertRaises(MissingVariableError) as cm:
            template.render(context)

        self.assertEqual(str(cm.exception), "'name' missing in 'index.html'")

    def test_ignored_prefix(self):
        template = Template("Hi {{ name }}", name="admin/index.html")
        context = Context({"nome": "Adam"})

        result = template.render(context)

        self.assertEqual(result, "Hi ")

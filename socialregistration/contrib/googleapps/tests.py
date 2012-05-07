from django import template
from django.conf import settings
from django.test import TestCase


class TestTemplateTag(TestCase):
    def test_tag_renders_correctly(self):
        tpl = """{% load googleapps %}{% googleapps_form %}"""

        self.assertTrue('form' in template.Template(tpl).render(template.Context({'request': None})))

        tpl = """{% load googleapps %}{% googleapps_form "example.com" "image/for/google.jpg" %}"""

        self.assertTrue('example.com' in template.Template(tpl).render(template.Context({'request': None})))
        self.assertTrue('image/for/google.jpg' in template.Template(tpl).render(template.Context({'request': None})))


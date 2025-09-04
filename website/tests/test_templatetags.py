import tempfile
from pathlib import Path

from django.conf import settings
from django.template import Context, Template
from django.test import TestCase


class TemplateTagsTest(TestCase):
    def test_replace_word_filter(self):
        tpl = Template('{% load replace_word %}{{ "vendo"|replace_word }}')
        rendered = tpl.render(Context({}))
        # replace_word replaces last two chars with 'ndo'
        self.assertEqual(rendered, "venndo")

    def test_get_tile_types_fallback_dirs(self):
        # create a temp templates directory with tiles
        tmpd = tempfile.TemporaryDirectory()
        tiles = Path(tmpd.name) / "tiles"
        tiles.mkdir()
        # create two tile templates
        (tiles / "tile_small.html").write_text("<div>small</div>")
        (tiles / "tile_large.html").write_text("<div>large</div>")

        # patch settings TEMPLATES DIRS to include tmpd
        orig_templates = settings.TEMPLATES
        new_templates = []
        for t in orig_templates:
            cfg = dict(t)
            cfg["DIRS"] = [tmpd.name]
            new_templates.append(cfg)

        settings.TEMPLATES = new_templates

        try:
            # import tag and call it via template rendering
            tpl = Template(
                (
                    "{% load get_type %}{% get_tile_types as tile_types %}"
                    "{{ tile_types|length }}"
                )
            )
            rendered = tpl.render(Context({}))
            # should find both tile files
            self.assertIn("2", rendered)
        finally:
            settings.TEMPLATES = orig_templates
            tmpd.cleanup()

from unittest import skipIf

from django.test import SimpleTestCase

from website.utils.sanitizer import CSS_SANITIZER, sanitize_html


class SanitizeHtmlIframeAttributesTests(SimpleTestCase):
    def test_iframe_keeps_width_and_height_without_style(self):
        html = '<iframe src="https://www.youtube.com/embed/abc12345678" width="640" height="360"></iframe>'
        cleaned = sanitize_html(html)

        self.assertIn('width="640"', cleaned)
        self.assertIn('height="360"', cleaned)


@skipIf(CSS_SANITIZER is None, "tinycss2 required for inline style sanitization")
class SanitizeHtmlIframeStyleTests(SimpleTestCase):
    def test_iframe_keeps_width_height_and_safe_style(self):
        html = (
            '<iframe src="https://www.youtube.com/embed/abc12345678" '
            'width="640" height="360" style="width: 640px; height: 360px; position: fixed"></iframe>'
        )
        cleaned = sanitize_html(html)

        self.assertIn('width="640"', cleaned)
        self.assertIn('height="360"', cleaned)
        self.assertIn("width: 640px", cleaned)
        self.assertIn("height: 360px", cleaned)
        self.assertNotIn("position", cleaned)

    def test_iframe_strips_unsafe_style_properties(self):
        html = '<iframe src="https://www.youtube.com/embed/abc12345678" style="background: url(javascript:alert(1))"></iframe>'
        cleaned = sanitize_html(html)

        self.assertNotIn("javascript", cleaned)

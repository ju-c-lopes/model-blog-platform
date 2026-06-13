from unittest import skipIf

from django import forms
from django.test import SimpleTestCase, TestCase

from website.forms.post.PostForm import PostForm
from website.utils.sanitizer import CSS_SANITIZER, SanitizerError, sanitize_html


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


@skipIf(CSS_SANITIZER is None, "tinycss2 required for inline style sanitization")
class SanitizeHtmlQuillTests(SimpleTestCase):
    def test_code_block_container_preserved(self):
        html = '<div class="ql-code-block-container">print("hi")</div>'
        cleaned = sanitize_html(html)
        self.assertIn('class="ql-code-block-container"', cleaned)
        self.assertIn("print", cleaned)

    def test_list_with_data_list_and_ql_ui_preserved(self):
        html = '<ol><li data-list="bullet" class="ql-indent-1"><span class="ql-ui"></span>Item</li></ol>'
        cleaned = sanitize_html(html)
        self.assertIn('data-list="bullet"', cleaned)
        self.assertIn('class="ql-indent-1"', cleaned)
        self.assertIn('class="ql-ui"', cleaned)
        self.assertIn("Item", cleaned)

    def test_align_and_indent_classes_on_paragraph(self):
        html = '<p class="ql-align-center ql-indent-2">Centered</p>'
        cleaned = sanitize_html(html)
        self.assertIn('class="ql-align-center ql-indent-2"', cleaned)

    def test_colored_span_preserved(self):
        html = '<p><span style="color: rgb(230, 0, 0);">red</span></p>'
        cleaned = sanitize_html(html)
        self.assertIn("<span", cleaned)
        self.assertIn("color:", cleaned)
        self.assertIn("red", cleaned)

    def test_underline_and_strike_preserved(self):
        html = "<p><u>underline</u> <s>strike</s></p>"
        cleaned = sanitize_html(html)
        self.assertIn("<u>underline</u>", cleaned)
        self.assertIn("<s>strike</s>", cleaned)

    def test_font_class_preserved(self):
        html = '<p><span class="ql-font-serif">serif</span></p>'
        cleaned = sanitize_html(html)
        self.assertIn('class="ql-font-serif"', cleaned)

    def test_strips_non_quill_classes(self):
        html = '<p class="ql-align-center evil">text</p>'
        cleaned = sanitize_html(html)
        self.assertIn('class="ql-align-center"', cleaned)
        self.assertNotIn("evil", cleaned)

    def test_executable_script_removed(self):
        html = "<p>ok</p><script>alert(1)</script>"
        cleaned = sanitize_html(html)
        self.assertIn("ok", cleaned)
        self.assertNotIn("alert", cleaned)
        self.assertNotIn("<script>", cleaned)


class SanitizeHtmlLdJsonTests(SimpleTestCase):
    def test_valid_ld_json_preserved(self):
        html = (
            '<p>Post</p><script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"Article","headline":"T"}'
            "</script>"
        )
        cleaned = sanitize_html(html)
        self.assertIn('type="application/ld+json"', cleaned)
        self.assertIn('"@type":"Article"', cleaned)
        self.assertIn("Post", cleaned)

    def test_invalid_ld_json_raises(self):
        html = '<script type="application/ld+json">{ not json }</script>'
        with self.assertRaises(SanitizerError):
            sanitize_html(html)

    def test_ld_json_reserialized(self):
        html = '<script type="application/ld+json">  { "a" : 1 }  </script>'
        cleaned = sanitize_html(html)
        self.assertIn('{"a":1}', cleaned)


class PostFormSanitizerIntegrationTests(TestCase):
    def test_invalid_ld_json_raises_on_clean_text(self):
        form = PostForm()
        form.cleaned_data = {
            "text": '<script type="application/ld+json">{bad}</script><p>Conteúdo suficiente aqui.</p>'
        }
        with self.assertRaises(forms.ValidationError):
            form.clean_text()

    def test_valid_ld_json_in_clean_text(self):
        form = PostForm()
        form.cleaned_data = {
            "text": (
                '<script type="application/ld+json">{"@type":"Article"}</script>'
                "<p>Conteúdo suficiente para validação.</p>"
            )
        }
        cleaned = form.clean_text()
        self.assertIn("application/ld+json", cleaned)
        self.assertIn("Conteúdo suficiente", cleaned)

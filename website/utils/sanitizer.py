"""
Small sanitizer utility using bleach to clean user-provided HTML.

This centralizes allowed tags/attributes and can be tuned later.
"""

from __future__ import annotations

import re

import bleach

try:
    from bleach.css_sanitizer import CSSSanitizer

    CSS_SANITIZER = CSSSanitizer(
        allowed_css_properties=[
            "width",
            "height",
            "max-width",
            "max-height",
            "min-width",
            "min-height",
            "aspect-ratio",
            "margin",
            "margin-top",
            "margin-bottom",
            "margin-left",
            "margin-right",
            "display",
            "border",
            "border-radius",
            "color",
            "background-color",
        ]
    )
except ImportError:
    CSS_SANITIZER = None

ALLOWED_DATA_LIST = frozenset({"bullet", "ordered", "checked", "unchecked"})
QUILL_CLASS_PREFIX = "ql-"
QUILL_CLASS_EXACT = frozenset({"ql-code-block-container", "ql-code-block"})

LD_JSON_SCRIPT_RE = re.compile(
    r"<script\b[^>]*\btype\s*=\s*['\"]application/ld\+json['\"][^>]*>(.*?)</script>",
    re.IGNORECASE | re.DOTALL,
)
ANY_SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL)
CLASS_ATTR_RE = re.compile(r'(\s+)class="([^"]*)"', re.IGNORECASE)
DATA_LIST_ATTR_RE = re.compile(r'(\s+)data-list="([^"]*)"', re.IGNORECASE)

ALLOWED_TAGS = [
    "a",
    "b",
    "blockquote",
    "br",
    "code",
    "em",
    "i",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "span",
    "strong",
    "u",
    "ul",
    "img",
    "iframe",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "table",
    "tbody",
    "tr",
    "td",
    "div",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title", "width", "height", "style"],
    "iframe": ["src", "width", "height", "frameborder", "allow", "allowfullscreen", "style"],
    "td": ["colspan", "rowspan", "data-row", "data-col"],
    "div": ["style", "class"],
    "span": ["class", "style"],
    "p": ["class"],
    "h1": ["class"],
    "h2": ["class"],
    "h3": ["class"],
    "h4": ["class"],
    "h5": ["class"],
    "h6": ["class"],
    "li": ["class", "data-list"],
    "ol": ["class"],
    "ul": ["class"],
    "code": ["class"],
    "pre": ["class"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto", "data"]
LINKIFY = True


class SanitizerError(ValueError):
    """Raised when user HTML cannot be safely sanitized."""


def _filter_quill_class(class_value: str) -> str:
    kept = []
    for token in class_value.split():
        if token in QUILL_CLASS_EXACT or token.startswith(QUILL_CLASS_PREFIX):
            kept.append(token)
    return " ".join(kept)


def _normalize_quill_attributes(html: str) -> str:
    def clean_class(match: re.Match[str]) -> str:
        prefix, value = match.group(1), match.group(2)
        filtered = _filter_quill_class(value)
        if filtered:
            return f'{prefix}class="{filtered}"'
        return ""

    def clean_data_list(match: re.Match[str]) -> str:
        prefix, value = match.group(1), match.group(2)
        if value in ALLOWED_DATA_LIST:
            return f'{prefix}data-list="{value}"'
        return ""

    html = CLASS_ATTR_RE.sub(clean_class, html)
    return DATA_LIST_ATTR_RE.sub(clean_data_list, html)


def _render_ld_json_script(data) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{payload}</script>'


def _extract_ld_json_scripts(html: str) -> tuple[str, list[str]]:
    """Return HTML with ld+json placeholders removed and list of canonical script tags."""
    scripts: list[str] = []
    invalid_blocks: list[str] = []

    def replace_ld_json(match: re.Match[str]) -> str:
        raw = match.group(1).strip()
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            invalid_blocks.append(raw[:80])
            return ""
        scripts.append(_render_ld_json_script(parsed))
        return ""

    without_ld_json = LD_JSON_SCRIPT_RE.sub(replace_ld_json, html)
    if invalid_blocks:
        raise SanitizerError("JSON-LD inválido em script application/ld+json. Verifique a sintaxe JSON na aba HTML.")

    without_scripts = ANY_SCRIPT_RE.sub("", without_ld_json)
    if without_scripts != without_ld_json:
        # Non-LD scripts were stripped silently (executable script blocked).
        pass

    return without_scripts, scripts


def sanitize_html(value: str) -> str:
    """Return a cleaned HTML string safe for storage and rendering."""
    if not value:
        return value

    value = "".join(ch for ch in value if ord(ch) >= 32 or ch == "\n" or ch == "\t")

    html_without_scripts, ld_json_scripts = _extract_ld_json_scripts(value)
    html_without_scripts = _normalize_quill_attributes(html_without_scripts)

    cleaned = bleach.clean(
        html_without_scripts,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        css_sanitizer=CSS_SANITIZER,
        strip=True,
    )

    if LINKIFY:
        cleaned = bleach.linkify(cleaned)

    if ld_json_scripts:
        if cleaned:
            cleaned = f"{cleaned}\n{''.join(ld_json_scripts)}"
        else:
            cleaned = "".join(ld_json_scripts)

    return cleaned

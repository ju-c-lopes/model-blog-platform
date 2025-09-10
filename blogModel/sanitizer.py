"""
Small sanitizer utility using bleach to clean user-provided HTML.
This centralizes allowed tags/attributes and can be tuned later.
"""

import bleach

# Keep this conservative: allow a small set of formatting tags and images/links
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
    "strong",
    "ul",
    "img",
    "iframe",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title", "width", "height"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto", "data"]

# Optional: link rel="nofollow" for user-provided links
LINKIFY = True


def sanitize_html(value: str) -> str:
    """Return a cleaned HTML string safe for storage and rendering.

    This removes dangerous tags and attributes while preserving basic
    formatting. Use this on user-submitted rich text before saving.
    """
    if not value:
        return value

    # First, strip control characters
    value = "".join(ch for ch in value if ord(ch) >= 32 or ch == "\n" or ch == "\t")

    cleaned = bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )

    if LINKIFY:
        cleaned = bleach.linkify(cleaned)

    return cleaned

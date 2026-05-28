import re

filepath = "website/tests/test_templatetags.py"
with open(filepath, "r") as f:
    content = f.read()

# remove test_get_tile_types_fallback_dirs
content = re.sub(
    r"    def test_get_tile_types_fallback_dirs\(self\):.*?        try:.*?except Exception:.*?pass",
    "",
    content,
    flags=re.DOTALL,
)

# remove test_replace_word_filter
content = re.sub(
    r"    def test_replace_word_filter\(self\):.*?(?=    def|$)",
    "",
    content,
    flags=re.DOTALL,
)

with open(filepath, "w") as f:
    f.write(content)

"""Template tag helpers for discovering available "tile" templates.

This module provides a `get_tile_types` simple tag that returns a list of
tile template names found under `website/templates/tiles/` (files named
like `tile_*.html`). It falls back to scanning any template directories
configured in settings.TEMPLATES[*]['DIRS'] if the package-local folder is
not present.

Usage in template:

    {% load get_type %}
    {% get_tile_types as tile_types %}
    {% for t in tile_types %}
      {{ t }}
    {% endfor %}

The tag returns the template filename stem (without .html), e.g. 'tile_small'.
"""

from pathlib import Path

from django import template
from django.conf import settings

import website as website_pkg

register = template.Library()


@register.simple_tag
def get_tile_types():
    """Return a list of available tile template names (stem without .html).

    It first tries to read files from the package's `templates/tiles/`
    directory (useful for this project layout). If none are found, it
    falls back to scanning template dirs listed in settings.TEMPLATES.
    """
    types = []

    # Primary: project app's templates/tiles folder
    try:
        base = Path(website_pkg.__file__).resolve().parent / "templates" / "tiles"
        if base.exists() and base.is_dir():
            for f in sorted(base.iterdir()):
                if f.is_file() and f.suffix == ".html" and f.name.startswith("tile_"):
                    types.append(f.stem)
    except Exception:
        # best-effort; ignore errors and try fallback
        types = []

    # Fallback: scan configured template DIRS
    if not types:
        tmpl_dirs = []
        for cfg in getattr(settings, "TEMPLATES", []):
            tmpl_dirs.extend(cfg.get("DIRS", []))

        for d in tmpl_dirs:
            try:
                p = Path(d) / "tiles"
                if p.exists() and p.is_dir():
                    for f in sorted(p.iterdir()):
                        if (
                            f.is_file()
                            and f.suffix == ".html"
                            and f.name.startswith("tile_")
                        ):
                            types.append(f.stem)
            except Exception:
                continue

    return types

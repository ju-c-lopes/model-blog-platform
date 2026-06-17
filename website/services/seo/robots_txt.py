"""
Regras do robots.txt.

Ordem importa: blocos com user-agent ESPECÍFICO vêm ANTES do "*" (catch-all).
Para um novo crawler (ex.: Googlebot), insira um dict acima do bloco "*".

O noindex impede indexação; omitir no robots economiza crawl budget só se quiser
bloquear rastreamento — hoje permitimos crawl, bloqueamos indexação via HTML.

/nossa-equipe/*/edit usa wildcard suportado pelo Google/Bing para bloquear
edição de perfil de autor sem bloquear /nossa-equipe/<slug>/ público.

/atualizar-perfil/ — fluxo legado ProfileUpdateView (@login_required); ainda
existe e é testado; edição principal hoje é /nossa-equipe/<slug>/edit e
/editar-leitor/.
"""

from __future__ import annotations

from typing import TypedDict


class RobotsRuleBlock(TypedDict, total=False):
    user_agent: str
    allow: list[str]
    disallow: list[str]


# Blocos específicos primeiro; "*" sempre por último.
ROBOTS_RULES: list[RobotsRuleBlock] = [
    # {
    #     "user_agent": "Googlebot",
    #     "allow": ["/"],
    #     "disallow": ["/exemplo/"],
    # },
    {
        "user_agent": "*",
        "allow": ["/"],
        "disallow": [
            "/admin/",
            "/accounts/",
            "/login/",
            "/cadastre-se/",
            "/solicitar-autor/",
            "/atualizar-perfil/",
            "/editar-leitor/",
            "/logout/",
            "/post/create/",
            "/post/edit/",
            "/post/upload-content-image/",
            "/nossa-equipe/*/edit",
            "/seo/",
            "/error/",
        ],
    },
]


def build_robots_txt_body(sitemap_url: str) -> str:
    lines: list[str] = []

    for block in ROBOTS_RULES:
        lines.append(f"User-agent: {block['user_agent']}")
        lines.append("")
        for path in block.get("allow", []):
            lines.append(f"Allow: {path}")
        lines.append("")
        for path in block.get("disallow", []):
            lines.append(f"Disallow: {path}")
        lines.append("")

    lines.append(f"Sitemap: {sitemap_url}")
    return "\n".join(lines)

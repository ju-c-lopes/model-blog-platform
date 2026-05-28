# Organização dos estilos (`website/static/css`)

Espelha a separação por domínio do projeto (models, views, forms, scripts).

| Pasta | Responsabilidade | Arquivos |
|-------|------------------|----------|
| `base/` | Layout global, tipografia, container | `base.css`, `header.css` |
| `author/` | Páginas do autor (equipe, perfil público, edição) | `author-page.css`, `edit.css` |
| `reader/` | Páginas do leitor (edição de perfil) | `edit.css` |
| `post/` | Posts (detalhe, editor, busca) | `post.css`, `edit_post.css`, `search.css` |
| `user/` | Autenticação e cadastro (`views/user`) | `login.css`, `sign-up.css` |
| `pages/` | Páginas gerais sem domínio único | `home.css` |
| `exceptions/` | Páginas de erro HTTP | `error.css` |

Vendor (Bootstrap, Quill): `website/static/vendor/`, referenciado nos templates do editor.

## Onde cada CSS é carregado

- `base/*` → `blog/pages/base.html`
- `author/author-page.css` → `author/author.html`, `our-team/our-team.html`, `post/post_detail.html` (card do autor)
- `author/edit.css` → `edit-author/edit-author.html`
- `reader/edit.css` → `edit-reader/edit-reader.html`
- `post/post.css` → `post/post_detail.html`, `post/edit_post.html`
- `post/edit_post.css` → `post/edit_post.html`
- `post/search.css` → `search/search_results.html`
- `user/login.css` → `login/login.html`
- `user/sign-up.css` → `sign-up/sign-up.html`, `profile-update/update-profile.html`
- `pages/home.css` → `home-page/homepage.html`, `search/search_results.html`
- `exceptions/error.css` → `errors/403.html`, `errors/404.html`, `errors/500.html`

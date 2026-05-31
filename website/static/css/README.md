# Organização dos estilos (`website/static/css`)

Espelha a separação por domínio do projeto (models, views, forms, scripts).

| Pasta | Responsabilidade | Arquivos |
|-------|------------------|----------|
| `base/` | Layout global, tipografia, container | `base.css`, `header.css` |
| `shared/` | Estilos reutilizados entre domínios | `edit-profile.css` |
| `author/` | Páginas do autor (equipe, perfil público, edição) | `author-page.css`, `edit.css`, `edit-formsets.css` |
| `reader/` | Páginas do leitor (edição de perfil) | `edit.css` |
| `post/` | Posts (detalhe, editor, busca) | `post.css`, `edit_post.css`, `search.css` |
| `user/` | Autenticação e cadastro (`views/user`) | `login.css`, `sign-up.css` |
| `pages/` | Páginas gerais sem domínio único | `home.css` |
| `exceptions/` | Páginas de erro HTTP | `error.css` |

Vendor (Bootstrap, Quill): `website/static/vendor/`, referenciado nos templates do editor.

## Edição de perfil (author + reader)

Camada compartilhada em `shared/edit-profile.css`:

- Variáveis, `.form-table`, `.form-field-row`, inputs, selects, textarea
- Layout da página (`.edit-form`, `.edit-user`, `.author-form`, `.reader-form`, `.save-button`)
- Media queries: mobile → tablet → desktop

Camada author em `author/edit-formsets.css`:

- Formsets (social, jobs, graduation), checkboxes, botões `+`

Entrada por página:

- `author/edit.css` → `@import` shared + formsets → `edit-author/edit-author.html`
- `reader/edit.css` → `@import` shared → `edit-reader/edit-reader.html`

## Demais CSS

- `base/*` → `blog/pages/base.html`
- `author/author-page.css` → `author/author.html`, `our-team/our-team.html`, `post/post_detail.html` (card do autor)
- `post/post.css` → `post/post_detail.html`, `post/edit_post.html`
- `post/edit_post.css` → `post/edit_post.html`
- `post/search.css` → `search/search_results.html`
- `user/login.css` → `login/login.html`
- `user/sign-up.css` → `sign-up/sign-up.html`, `profile-update/update-profile.html`
- `pages/home.css` → `home-page/homepage.html`, `search/search_results.html`
- `exceptions/error.css` → `errors/403.html`, `errors/404.html`, `errors/500.html`

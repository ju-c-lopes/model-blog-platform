import re

from django import forms
from django.utils.text import slugify

from website.models.post.PostModel import Post
from website.models.post.TagModel import Tag
from website.utils.sanitizer import sanitize_html


class PostForm(forms.ModelForm):
    """Formulário de criação e edição de posts com editor rich text."""

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.MultipleHiddenInput,
        label="Tags",
        help_text="Tecnologias ou temas abordados no post.",
    )

    class Meta:
        model = Post
        fields = ["title", "url_slug", "meta_description", "cover_image", "tags", "text"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título envolvente do post",
                    "maxlength": "200",
                }
            ),
            "url_slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "meu-post-incrivel",
                    "pattern": "[a-z0-9-]+",
                    "title": "Use apenas letras minúsculas, números e hífens",
                }
            ),
            "meta_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descrição para SEO (máx. 160 caracteres)",
                    "rows": 3,
                    "maxlength": "160",
                }
            ),
            "cover_image": forms.FileInput(
                attrs={
                    "class": "form-control-file",
                    "accept": "image/*",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "form-control rich-text-editor",
                    "id": "rich-editor",
                    "placeholder": "Comece a escrever o conteúdo aqui...",
                }
            ),
        }
        labels = {
            "title": "Título",
            "url_slug": "URL amigável (slug)",
            "meta_description": "Meta descrição (SEO)",
            "cover_image": "Imagem de capa",
            "text": "Conteúdo",
        }
        help_texts = {
            "url_slug": "Identificador único na URL (letras minúsculas, números e hífens)",
            "meta_description": "Aparece nos resultados de busca. Mantenha até 160 caracteres.",
            "cover_image": "Imagem exibida em listagens e no topo do post (opcional).",
            "text": "Use o editor para formatar o conteúdo com títulos, imagens, vídeos e tabelas.",
        }

    def clean_url_slug(self):
        url_slug = self.cleaned_data.get("url_slug")
        url_slug = url_slug.lower().replace(" ", "-")
        url_slug = re.sub(r"[^a-z0-9-]", "", url_slug)
        url_slug = re.sub(r"-+", "-", url_slug)
        url_slug = url_slug.strip("-")

        if not url_slug:
            raise forms.ValidationError("O slug não pode ficar vazio após a formatação.")

        if self.instance.pk:
            if Post.objects.filter(url_slug=url_slug).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este slug já está em uso. Escolha outro.")
        elif Post.objects.filter(url_slug=url_slug).exists():
            raise forms.ValidationError("Este slug já está em uso. Escolha outro.")

        return url_slug

    def clean_meta_description(self):
        meta_description = self.cleaned_data.get("meta_description")
        if meta_description and len(meta_description) > 160:
            raise forms.ValidationError("A meta descrição deve ter no máximo 160 caracteres.")
        return meta_description

    def clean(self):
        cleaned_data = super().clean()
        self._new_tag_names = []
        seen = set()

        for raw_name in self.data.getlist("new_tag_names"):
            name = raw_name.strip()
            if not name:
                continue

            key = name.casefold()
            if key in seen:
                continue
            seen.add(key)

            if len(name) > Tag._meta.get_field("name").max_length:
                self.add_error(
                    "tags",
                    forms.ValidationError(f'A tag "{name[:20]}…" excede o limite de 50 caracteres.'),
                )
                continue

            if not slugify(name):
                self.add_error("tags", forms.ValidationError(f'Não foi possível gerar slug para "{name}".'))
                continue

            self._new_tag_names.append(name)

        return cleaned_data

    def clean_text(self):
        text = self.cleaned_data.get("text")
        try:
            return sanitize_html(text)
        except Exception:
            return text

    def save(self, commit=True):
        old_cover = None
        if self.instance.pk and "cover_image" in self.changed_data:
            old_cover = Post.objects.only("cover_image").get(pk=self.instance.pk).cover_image

        instance = super().save(commit=False)

        if commit:
            instance.save()
            self._save_m2m()

            if old_cover and old_cover != instance.cover_image:
                old_cover.delete(save=False)

        return instance

    def _save_m2m(self):
        self._save_tags(self.instance)

    def _save_tags(self, instance):
        tags = list(self.cleaned_data.get("tags") or [])
        tag_ids = {tag.pk for tag in tags}

        for name in getattr(self, "_new_tag_names", []):
            tag, _created = Tag.objects.get_or_create(
                slug=slugify(name),
                defaults={"name": name, "icon": ""},
            )
            if tag.pk not in tag_ids:
                tags.append(tag)
                tag_ids.add(tag.pk)

        instance.tags.set(tags)

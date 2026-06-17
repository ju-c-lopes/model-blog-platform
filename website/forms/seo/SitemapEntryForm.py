from django import forms

from website.models.seo.SitemapEntryModel import SitemapEntry
from website.services.seo.sitemap_builder import normalize_path


class SitemapPathForm(forms.Form):
    path = forms.CharField(
        max_length=500,
        label="URL",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "/post/exemplo/"}),
    )
    notes = forms.CharField(
        max_length=255,
        required=False,
        label="Notas",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def clean_path(self):
        return normalize_path(self.cleaned_data["path"])


class SitemapIncludeForm(SitemapPathForm):
    lastmod = forms.DateTimeField(
        required=False,
        label="Última modificação (lastmod)",
        widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
    )

    def save(self) -> SitemapEntry:
        return SitemapEntry.objects.update_or_create(
            path=self.cleaned_data["path"],
            defaults={
                "entry_type": SitemapEntry.INCLUDE,
                "lastmod": self.cleaned_data.get("lastmod"),
                "notes": self.cleaned_data.get("notes", ""),
                "is_active": True,
            },
        )[0]


class SitemapExcludeForm(SitemapPathForm):
    def save(self) -> SitemapEntry:
        return SitemapEntry.objects.update_or_create(
            path=self.cleaned_data["path"],
            defaults={
                "entry_type": SitemapEntry.EXCLUDE,
                "notes": self.cleaned_data.get("notes", ""),
                "is_active": True,
            },
        )[0]

import importlib

MODULES = [
    "website.views.author.AuthorView",
    "website.views.user.LoginView",
    "website.views.post.SearchView",
    "website.views.author.AuthorEditView",
    "website.views.post.PostCreateView",
    "website.models.author.AuthorModel",
    "website.models.post.PostModel",
    "website.models.user.ReaderModel",
    "website.forms.author.EditAuthorForm",
    "website.forms.author.author_edit_formsets",
    "website.services.author.author_profile_editor",
    "website.services.reader.reader_profile_editor",
    "website.forms.post.PostForm",
    "website.templatetags.get_type",
    "website.manager",
    "website.admin",
]


def test_quick_imports():
    errors = {}
    for mod in MODULES:
        try:
            importlib.import_module(mod)
        except Exception as e:
            errors[mod] = str(e)

    # At least main modules should import without error
    assert not errors, f"Import errors occurred: {errors}"

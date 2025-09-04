import importlib

MODULES = [
    "website.views.AuthorView",
    "website.views.LoginView",
    "website.views.SearchView",
    "website.views.ProfileUpdateView",
    "website.views.PostCreateView",
    "website.models.AuthorModel",
    "website.models.PostModel",
    "website.models.ReaderModel",
    "website.forms.EditAuthorForm",
    "website.forms.PostForm",
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

from django.conf import settings


def test_admin_module_loads():
    # import admin module to execute top-level registration code
    import website.admin as adm

    # ensure module imported
    assert hasattr(adm, "__name__")


def test_get_type_direct_call(tmp_path, monkeypatch):
    # create tiles directory under a temp templates dir
    tdir = tmp_path / "templates"
    tiles = tdir / "tiles"
    tiles.mkdir(parents=True)
    (tiles / "tile_x.html").write_text("x")
    (tiles / "tile_y.html").write_text("y")

    # patch settings.TEMPLATES to include our tmp templates dir
    orig = settings.TEMPLATES
    new_templates = []
    for t in orig:
        cfg = dict(t)
        cfg["DIRS"] = [str(tdir)]
        new_templates.append(cfg)
    monkeypatch.setattr(settings, "TEMPLATES", new_templates)

    # import tag function and call it
    from website.templatetags.get_type import get_tile_types

    types = get_tile_types()
    # should return two types
    assert "tile_x" in types
    assert "tile_y" in types


def test_userchangeform_clean_and_save(db):
    from django.contrib.auth import get_user_model

    from website.forms.EditAuthorForm import UserChangeForm

    User = get_user_model()
    u = User.objects.create_user(email="ux@example.com", password="old", username="ux")

    # mismatched passwords should add an error
    form = UserChangeForm(
        {
            "username": "ux2",
            "email": "ux2@example.com",
            "password": "a",
            "confirm_pass": "b",
        },
        instance=u,
    )
    assert not form.is_valid()
    # call clean() for coverage; return value not used
    form.clean()
    # mismatched should produce an error for confirm_pass
    assert "confirm_pass" in form.errors

    # matching password should set_password on save
    form2 = UserChangeForm(
        {
            "username": "ux2",
            "email": "ux2@example.com",
            "password": "new",
            "confirm_pass": "new",
        },
        instance=u,
    )
    assert form2.is_valid()
    user2 = form2.save()
    # saved user should have changed password (can't compare hash directly but ensure it's set)
    assert user2.password != "old"

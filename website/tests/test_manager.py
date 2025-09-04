from website.manager import UserManager


class DummyUser:
    def __init__(self, email=None, **extra):
        self.email = email
        self.extra = extra
        self.password = None
        self.saved = False

    def set_password(self, raw):
        self.password = raw

    def save(self):
        self.saved = True


def test_create_user_and_superuser_paths():
    mgr = UserManager()
    mgr.model = DummyUser

    # create_user happy path
    u = mgr.create_user("u@example.com", "secret")
    assert isinstance(u, DummyUser)
    assert u.email == "u@example.com"
    assert u.password == "secret"
    assert u.saved

    # create_superuser happy path (should call create_user)
    su = mgr.create_superuser("admin@example.com", "root")
    assert isinstance(su, DummyUser)
    assert su.email == "admin@example.com"
    assert su.password == "root"


def test_create_user_missing_email_raises():
    mgr = UserManager()
    mgr.model = DummyUser

    try:
        mgr.create_user("", "pw")
        raised = False
    except ValueError:
        raised = True

    assert raised


def test_create_superuser_checks_flags():
    mgr = UserManager()
    mgr.model = DummyUser

    # passing wrong flags should raise
    try:
        mgr.create_superuser("x@x.com", "pw", is_staff=False)
        ok = True
    except ValueError:
        ok = False

    assert not ok

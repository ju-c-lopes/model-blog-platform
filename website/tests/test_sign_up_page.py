from django.contrib import messages
from django.test import Client, RequestFactory, TestCase

from website.models import Author, Reader, User
from website.views.SignUpView import check_password_request, sign_up_user


class TestSignUpPageGet(TestCase):
    """
    Test for correct first access to sign up page
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_sign_up_access(self):
        request = self.factory.get("/cadastre-se/")
        page_accessed = sign_up_user(request)
        self.assertEqual(page_accessed.status_code, 200)


class TestSignUpUsers(TestCase):
    """
    Test creating an author user
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_password_force(self):
        pass1_to_match = "Abcdef123456#"
        pass2_equal = "Abcdef123456#"
        pass3_not_equal = "aBcdef123456@"
        pass4_short = "Abc123$"
        pass5_missing_upper = "abcdef123456#"
        pass6_missing_number = "abdCefghijk"
        pass7_missing_special = "abCdef123456"

        self.assertTrue(
            check_password_request(pass1_to_match, pass2_equal),
            "Passwords aren't matching.",
        )
        self.assertFalse(
            check_password_request(pass1_to_match, pass3_not_equal),
            "Check pass function is accepting different passwords.",
        )
        self.assertFalse(
            check_password_request(pass4_short, pass4_short),
            "Short password is being accepted.",
        )
        self.assertFalse(
            check_password_request(pass5_missing_upper, pass5_missing_upper),
            "Upper validation failed.",
        )
        self.assertFalse(
            check_password_request(pass6_missing_number, pass6_missing_number),
            "Number validation failed.",
        )
        self.assertFalse(
            check_password_request(pass7_missing_special, pass7_missing_special),
            "Special validation failed.",
        )

    def test_create_author(self):
        request = self.factory.post(
            "/cadastre-se/",
            {
                "nome": "Usuário Teste Author",
                "password1": "123456&abcDef",
                "password2": "123456&abcDef",
                "email": "author@gmail.com",
                "tipo-user": "author",
                "phone": "11999999999",
            },
            follow=True,
        )
        request._messages = messages.storage.default_storage(request)
        response = sign_up_user(request)
        response.client = Client()
        request.user = User.objects.get(email="author@gmail.com")
        author = Author.objects.get(user=request.user.id)
        response.client.login(username=author.user, password="123456")
        self.assertTrue(request.user, True)
        self.assertEqual(author.author_url_slug, "usuario-teste-author")
        self.assertTrue(author.access_level, 1)
        self.assertRedirects(
            response,
            "/login/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_create_reader(self):
        request = self.factory.post(
            "/cadastre-se/",
            {
                "nome": "Usuário Teste Reader",
                "password1": "123456abC?def",
                "password2": "123456abC?def",
                "email": "reader@gmail.com",
                "tipo-user": "reader",
                "phone": "11999999999",
            },
            follow=True,
        )
        request._messages = messages.storage.default_storage(request)
        response = sign_up_user(request)
        response.client = Client()
        request.user = User.objects.get(email="reader@gmail.com")
        reader = Reader.objects.get(user=request.user.id)
        response.client.login(username=reader.user, password="123456")
        self.assertEqual(reader.user.username, "usuario-user1")
        self.assertEqual(reader.reader_name, "Usuário Teste Reader")
        self.assertTrue(reader.access_level, 2)
        self.assertRedirects(
            response,
            "/login/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

from django.test import TestCase, RequestFactory, Client
from website.views.SignUpView import sign_up_user
from website.models import User, Reader, Author
from django.contrib import messages

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
    
    def test_create_author(self):
        request = self.factory.post("/cadastre-se/", {
            "nome": "Usuário Teste Author",
            "password1": "123456",
            "password2": "123456",
            "email": "author@gmail.com",
            "tipo-user": "author",
            "phone": "11999999999",
        }, follow=True)
        request._messages = messages.storage.default_storage(request)
        response = sign_up_user(request)
        response.client = Client()
        request.user = User.objects.get(email="author@gmail.com")
        author = Author.objects.get(user=request.user.id)
        response.client.login(username=author.user, password="123456")
        self.assertTrue(request.user, True)
        self.assertEqual(author.author_url_slug, "usuario-teste-author")
        self.assertTrue(author.access_level, 1)
        self.assertRedirects(response, "/login/", status_code=302, target_status_code=200, fetch_redirect_response=True)
    
    def test_create_reader(self):
        request = self.factory.post("/cadastre-se/", {
            "nome": "Usuário Teste Reader",
            "password1": "123456",
            "password2": "123456",
            "email": "reader@gmail.com",
            "tipo-user": "reader",
            "phone": "11999999999",
        }, follow=True)
        request._messages = messages.storage.default_storage(request)
        response = sign_up_user(request)
        response.client = Client()
        request.user = User.objects.get(email="reader@gmail.com")
        reader = Reader.objects.get(user=request.user.id)
        response.client.login(username=reader.user, password="123456")
        self.assertEqual(reader.user.username, "usuario-user1")
        self.assertEqual(reader.reader_name, "Usuário Teste Reader")
        self.assertTrue(reader.access_level, 2)
        self.assertRedirects(response, "/login/", status_code=302, target_status_code=200, fetch_redirect_response=True)

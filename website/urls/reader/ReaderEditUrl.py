from django.urls import path

from website.views.reader.ReaderEditView import reader_edit

# Montado em blogModel/urls.py sob prefixo editar-leitor/
urlpatterns = [
    path("", reader_edit, name="reader-edit"),
]

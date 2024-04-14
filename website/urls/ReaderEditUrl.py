from django.urls import path
from website.views.ReaderEditView import reader_edit

urlpatterns = [
    path('', reader_edit, name='reader-edit'),
]

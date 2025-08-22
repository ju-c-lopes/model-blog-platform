"""
URL configuration for projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
import debug_toolbar

# Import error handlers
from website.views.ErrorView import handler404, handler500, handler403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls.HomeUrl')),
    path('nossa-equipe/', include('website.urls.TeamUrl')),
    path('login/', include('website.urls.LoginUrl')),
    path('cadastre-se/', include('website.urls.SignUpUrl')),
    path('editar-leitor/', include('website.urls.ReaderEditUrl')),
    path('atualizar-perfil/', include('website.urls.ProfileUpdateUrl')),  # Unified profile management
    path('logout/', include('website.urls.LogoutUrl')),
    path('post/', include('website.urls.PostUrl')),
    path('error/', include('website.urls.ErrorUrl')),
    path('search/', include('website.urls.SearchUrl')),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configure error handlers
handler404 = 'website.views.ErrorView.handler404'
handler500 = 'website.views.ErrorView.handler500'
handler403 = 'website.views.ErrorView.handler403'

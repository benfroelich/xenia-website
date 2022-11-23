"""froelich_leon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.contrib.flatpages import views
#from home.views import HomeView
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('blog/', include('cmsblog.urls')),
    #path('', TemplateView.as_view(template_name='home/home.html')),
    #path('', HomeView.as_view()),
    path('admin/', admin.site.urls),
    #path('pages/', include('django.contrib.flatpages.urls')),
    #path('about/', views.flatpage, {'url': '/about/'}, name='about'),

    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('', include(wagtail_urls)),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),
    path('profile/', include('user_profile.urls')),

    re_path(r'^(?P<url>.*/)$', views.flatpage),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

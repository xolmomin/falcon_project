from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from root.settings import MEDIA_URL, MEDIA_ROOT


def handler404_view(request, exception, template_name='apps/404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path('', include('apps.urls')),
    path("i18n/", include("django.conf.urls.i18n"), name="set_language"),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('rosetta/', include('rosetta.urls'))

) + static(MEDIA_URL, document_root=MEDIA_ROOT)

handler404 = 'root.urls.handler404_view'

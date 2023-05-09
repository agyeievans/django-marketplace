from django.contrib import admin
from django.urls import path, include
from core.views import index, contact
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('item/', include('item.urls', namespace='item')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

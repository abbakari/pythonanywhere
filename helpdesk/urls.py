from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from helpdesk import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')),
    path('check_notification/', views.check_notification, name='check_notification'),
]

# Static and media files for both development and production
# Vercel handles static files through vercel.json routing
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

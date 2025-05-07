from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Add the new app to the list of installed apps
    path('', include('users.urls')),
    path('', include('audit_logs.urls')),
    path('', include('attendance_management.urls')),
    path('', include('csv_manager.urls')),
    path('', include('vacations.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('auth/', include('authentication.urls')),
    path('user/', include('customer.urls')),
    path('partner/', include('partner.urls')),
    path('dashboard/admin/', include('dashboard.urls')),
    # Database Backup
    path('backup', views.dbbackup, name='dbbackup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.error_404'

handler500 = 'core.views.error_500'
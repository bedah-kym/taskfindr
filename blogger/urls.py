"""blogger URL Configuration

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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('payus/', include('PAYMENT.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('API.urls')),
    path('', include('blog.urls')),
    path('', include('users.urls')),
    path('', include('taskmanager.urls')),
    path('verification/', include('verify_email.urls')),
    path('jet/', include('jet.urls', 'jet')),	
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

]
handler404 = 'blog.views.error_404_view'
handler403 = 'blog.views.error_403_view'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

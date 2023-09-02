"""
URL configuration for backend project.

"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/scripts/', include('scripts.urls')),  # Include the 'scripts.urls' here
]


"""
URL configuration for worlds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from worlds import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('worlds', views.world_list),
    path('worlds/<int:id>', views.world_detail),
    path('locations', views.location_list),
    path('locations/<int:id>', views.location_detail),
    path('characters', views.character_list),
    path('characters/<int:id>', views.character_detail),
    path('events', views.event_list),
    path('events/<int:id>', views.event_detail),
    path('webhook/', views.webhook, name='webhook')
]

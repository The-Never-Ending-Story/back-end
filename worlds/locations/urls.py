from django.contrib import admin
from django.urls import path
from Locations import views

urlpatterns = [
    path('/admin/', admin.site.urls),
    path('worlds/<int:world_id>/locations', views.location_list),
    path('worlds/<int:world_id>locations/<int:id>', views.location_detail),
]

from django.contrib import admin
from django.urls import path
from .views import get_recommendations,index

urlpatterns = [
    path('peterlight_admin/', admin.site.urls),
    path('get_recommendations/', get_recommendations, name="get_recommendations"),
    path('', index, name="index")
]

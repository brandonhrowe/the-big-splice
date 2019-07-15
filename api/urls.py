from django.urls import path
from api import views

urlpatterns = [
  path('all/', views.all_films, name="all_films"),
  path('random/', views.random, name="random")
]

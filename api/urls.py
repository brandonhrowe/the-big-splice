from django.urls import path
from api.views import AllFilmsView, RandomFilmView

urlpatterns = [
  path('all/', AllFilmsView.as_view()),
  path('random/', RandomFilmView.as_view())
]

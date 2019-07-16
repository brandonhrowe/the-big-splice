from django.urls import path
from api.views import AllFilmsView, RandomFilmView, GenerateRandomClipView, GenerateFinalFilmView

urlpatterns = [
  path('all/', AllFilmsView.as_view()),
  path('random/', RandomFilmView.as_view()),
  path('clips/', GenerateRandomClipView.as_view()),
  path('final/', GenerateFinalFilmView.as_view())
]

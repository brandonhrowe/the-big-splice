from django.urls import path
from api.views import AllFilmsView, RandomFilmView, GenerateRandomClipView, GenerateFinalFilmView, RemoveClipsAndMainView, RemoveClipsView, RemoveMainView

urlpatterns = [
  path('clips/remove/', RemoveClipsView.as_view()),
  path('final/remove/', RemoveMainView.as_view()),
  path('all/remove/', RemoveClipsAndMainView.as_view()),
  path('all/', AllFilmsView.as_view()),
  path('random/', RandomFilmView.as_view()),
  path('clips/', GenerateRandomClipView.as_view()),
  path('final/', GenerateFinalFilmView.as_view()),
]

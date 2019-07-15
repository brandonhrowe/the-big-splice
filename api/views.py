from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from api.models import Film

# Create your views here.
# @api_view(["GET"])
# def all_films(request):
#   films = Film.objects.all().values()
#   return Response(status=status.HTTP_200_OK, data={"data": films})

# @api_view(["GET"])
# def random(request):
#   film = Film.random_film.get_random_film()
#   return Response(status=status.HTTP_200_OK, data={"data": film})


class AllFilmsView(APIView):
    def get(self, request, format=None):
        films = Film.objects.all().values()
        return Response(status=status.HTTP_200_OK, data={"data": films})


class RandomFilmView(APIView):
    def get(self, request, format=None):
        film = Film.random_film.get_random_film()
        return Response(status=status.HTTP_200_OK, data={"data": film})

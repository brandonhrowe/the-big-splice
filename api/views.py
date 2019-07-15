import os
from threading import Timer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from api.models import Film
from random import randint
import ffmpy
# from api.serializer import FilmSerializer

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

class GenerateRandomClipView(APIView):
    def get(self, request, format=None):
        filmOne = Film.random_film.get_random_film()
        filmTwo = Film.random_film.get_random_film()
        filmThree = Film.random_film.get_random_film()

        filmOne_totalShots = len(filmOne['timecodes'])
        filmOne_random_idx = randint(0, round(filmOne_totalShots / 3))
        filmOne_end_tc = round(
            float(filmOne['timecodes'][filmOne_random_idx + randint(1, 3)]) - (2 / 29.97), 2)
        if float(filmOne_end_tc) - float(filmOne['timecodes'][filmOne_random_idx]) > 60:
            filmOne_end_tc = float(filmOne['timecodes'][filmOne_random_idx]) + 60
        elif float(filmOne_end_tc) - float(filmOne['timecodes'][filmOne_random_idx]) < 5:
            filmOne_end_tc = float(filmOne['timecodes'][filmOne_random_idx]) + 30

        filmTwo_totalShots = len(filmTwo['timecodes'])
        filmTwo_random_idx = randint(0, round(filmTwo_totalShots / 3))
        filmTwo_end_tc = round(
            float(filmTwo['timecodes'][filmTwo_random_idx + randint(1, 3)]) - (2 / 29.97), 2)
        if float(filmTwo_end_tc) - float(filmTwo['timecodes'][filmTwo_random_idx]) > 60:
            filmTwo_end_tc = float(filmTwo['timecodes'][filmTwo_random_idx]) + 60
        elif float(filmTwo_end_tc) - float(filmTwo['timecodes'][filmTwo_random_idx]) < 5:
            filmTwo_end_tc = float(filmTwo['timecodes'][filmTwo_random_idx]) + 30

        filmThree_totalShots = len(filmThree['timecodes'])
        filmThree_random_idx = randint(0, round(filmThree_totalShots / 3))
        filmThree_end_tc = round(
            float(filmThree['timecodes'][filmThree_random_idx + randint(1, 3)]) - (2 / 29.97), 2)
        if float(filmThree_end_tc) - float(filmThree['timecodes'][filmThree_random_idx]) > 60:
            filmThree_end_tc = float(filmThree['timecodes'][filmThree_random_idx]) + 60
        elif float(filmThree_end_tc) - float(filmThree['timecodes'][filmThree_random_idx]) < 5:
            filmThree_end_tc = float(filmThree['timecodes'][filmThree_random_idx]) + 30





        ff_filmOne = ffmpy.FFmpeg(
            inputs={filmOne['url']:
                    f'-ss {filmOne["timecodes"][filmOne_random_idx]} -to {filmOne_end_tc}'},
            outputs={"./public/media/_temp/filmOne_Clip.mp4": "-r 30000/1001 -vf scale=640x480,setsar=1:1 -b:v 5M -maxrate 10M -bufsize 1M"}
        )
        ff_filmOne.cmd
        ff_filmOne.run()

        ff_filmTwo = ffmpy.FFmpeg(
            inputs={filmTwo['url']:
                    f'-ss {filmTwo["timecodes"][filmTwo_random_idx]} -to {filmTwo_end_tc}'},
            outputs={"./public/media/_temp/filmTwo_Clip.mp4": "-r 30000/1001 -vf scale=640x480,setsar=1:1 -b:v 5M -maxrate 10M -bufsize 1M"}
        )
        ff_filmTwo.cmd
        ff_filmTwo.run()

        ff_filmThree = ffmpy.FFmpeg(
            inputs={filmThree['url']:
                    f'-ss {filmThree["timecodes"][filmThree_random_idx]} -to {filmThree_end_tc}'},
            outputs={"./public/media/_temp/filmThree_Clip.mp4": "-r 30000/1001 -vf scale=640x480,setsar=1:1 -b:v 5M -maxrate 10M -bufsize 1M"}
        )
        ff_filmThree.cmd
        ff_filmThree.run()

        ff_merge = ffmpy.FFmpeg(
            inputs={f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/public/media/BigSplice_ShotList.txt": "-safe 0 -f concat"},
            outputs={"./public/media/_temp/test_concat.mp4": "-c copy"}
        )

        ff_merge.cmd
        ff_merge.run()

        files_to_delete = ["./public/media/_temp/filmOne_Clip.mp4", "./public/media/_temp/filmTwo_Clip.mp4", "./public/media/_temp/filmThree_Clip.mp4"]

        def clearFiles(files):
            print("start of clearfiles call")
            for file in files:
                print(f"deleting: {file}")
                os.remove(file)
            print("files have been deleted")

        timer = Timer(5.0, clearFiles, [files_to_delete])

        timer.start()

        return Response(status=status.HTTP_201_CREATED)


# class AllFilmsView(generics.ListAPIView):
#     queryset = Film.objects.all()
#     serializer_class = FilmSerializer

# class RandomFilmView(generics.ListAPIView):
#     queryset = Film.random_film.get_random_film()
#     serializer_class = FilmSerializer

import os
from threading import Timer
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from api.models import Film
from random import randint
import ffmpy
import json
import time
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
        return Response(status=status.HTTP_200_OK, data={"films": films})


class RandomFilmView(APIView):
    def get(self, request, format=None):
        film = Film.random_film.get_random_film()
        return Response(status=status.HTTP_200_OK, data={"film": film})


class GenerateRandomClipView(APIView):
    def post(self, request, format=None):
        filmOne = Film.random_film.get_random_film()
        filmTwo = Film.random_film.get_random_film()
        filmThree = Film.random_film.get_random_film()

        filmOne_totalShots = len(filmOne['timecodes'])
        filmOne_random_idx = randint(0, filmOne_totalShots - 3)
        filmOne_end_tc = round(
            float(filmOne['timecodes'][filmOne_random_idx + randint(1, 3)]) - (2 / 29.97), 2)
        if float(filmOne_end_tc) - float(filmOne['timecodes'][filmOne_random_idx]) > 60:
            filmOne_end_tc = float(
                filmOne['timecodes'][filmOne_random_idx]) + 60
        elif float(filmOne_end_tc) - float(filmOne['timecodes'][filmOne_random_idx]) < 5:
            filmOne_end_tc = float(
                filmOne['timecodes'][filmOne_random_idx]) + 30

        filmTwo_totalShots = len(filmTwo['timecodes'])
        filmTwo_random_idx = randint(0, filmTwo_totalShots - 3)
        filmTwo_end_tc = round(
            float(filmTwo['timecodes'][filmTwo_random_idx + randint(1, 3)]) - (2 / 29.97), 2)
        if float(filmTwo_end_tc) - float(filmTwo['timecodes'][filmTwo_random_idx]) > 60:
            filmTwo_end_tc = float(
                filmTwo['timecodes'][filmTwo_random_idx]) + 60
        elif float(filmTwo_end_tc) - float(filmTwo['timecodes'][filmTwo_random_idx]) < 5:
            filmTwo_end_tc = float(
                filmTwo['timecodes'][filmTwo_random_idx]) + 30

        filmThree_totalShots = len(filmThree['timecodes'])
        filmThree_random_idx = randint(0, filmThree_totalShots - 3)
        filmThree_end_tc = round(
            float(filmThree['timecodes'][filmThree_random_idx + randint(1, 3)]) - (2 / 29.97), 2)
        if float(filmThree_end_tc) - float(filmThree['timecodes'][filmThree_random_idx]) > 60:
            filmThree_end_tc = float(
                filmThree['timecodes'][filmThree_random_idx]) + 60
        elif float(filmThree_end_tc) - float(filmThree['timecodes'][filmThree_random_idx]) < 5:
            filmThree_end_tc = float(
                filmThree['timecodes'][filmThree_random_idx]) + 30

        filmOne_fileName = f"Clip1_{filmOne['identifier']}_{''.join(str(filmOne['timecodes'][filmOne_random_idx]).split('.'))}_{''.join(str(filmOne_end_tc).split('.'))}_{randint(0, 1000000)}"

        ff_filmOne = ffmpy.FFmpeg(
            inputs={filmOne['url']:
                    f'-ss {filmOne["timecodes"][filmOne_random_idx]} -to {filmOne_end_tc}'},
            outputs={f"./public/media/_temp/{filmOne_fileName}.mp4":
                     "-r 30000/1001 -vf scale=640x480,setsar=1:1 -b:v 5M -maxrate 10M -bufsize 1M -c:a aac -b:a 128k -ar 44100"}
        )
        ff_filmOne.cmd
        ff_filmOne.run()

        filmTwo_fileName = f"Clip2_{filmTwo['identifier']}_{''.join(str(filmTwo['timecodes'][filmTwo_random_idx]).split('.'))}_{''.join(str(filmTwo_end_tc).split('.'))}_{randint(0, 1000000)}"

        ff_filmTwo = ffmpy.FFmpeg(
            inputs={filmTwo['url']:
                    f'-ss {filmTwo["timecodes"][filmTwo_random_idx]} -to {filmTwo_end_tc}'},
            outputs={f"./public/media/_temp/{filmTwo_fileName}.mp4":
                     "-r 30000/1001 -vf scale=640x480,setsar=1:1 -b:v 5M -maxrate 10M -bufsize 1M -c:a aac -b:a 128k -ar 44100"}
        )
        ff_filmTwo.cmd
        ff_filmTwo.run()

        filmThree_fileName = f"Clip3_{filmThree['identifier']}_{''.join(str(filmThree['timecodes'][filmThree_random_idx]).split('.'))}_{''.join(str(filmThree_end_tc).split('.'))}_{randint(0, 1000000)}"

        ff_filmThree = ffmpy.FFmpeg(
            inputs={filmThree['url']:
                    f'-ss {filmThree["timecodes"][filmThree_random_idx]} -to {filmThree_end_tc}'},
            outputs={f"./public/media/_temp/{filmThree_fileName}.mp4":
                     "-r 30000/1001 -vf scale=640x480,setsar=1:1 -b:v 5M -maxrate 10M -bufsize 1M -c:a aac -b:a 128k -ar 44100"}
        )
        ff_filmThree.cmd
        ff_filmThree.run()

        ff_thumbnailOne = ffmpy.FFmpeg(
            inputs={f"./public/media/_temp/{filmOne_fileName}.mp4": f"-ss 1"},
            outputs={f"./public/media/_temp/{filmOne_fileName}_Thumbnail.jpg": f"-vframes 1"}
        )
        ff_thumbnailOne.cmd
        ff_thumbnailOne.run()

        ff_thumbnailTwo = ffmpy.FFmpeg(
            inputs={f"./public/media/_temp/{filmTwo_fileName}.mp4": f"-ss 1"},
            outputs={f"./public/media/_temp/{filmTwo_fileName}_Thumbnail.jpg": f"-vframes 1"}
        )
        ff_thumbnailTwo.cmd
        ff_thumbnailTwo.run()

        ff_thumbnailThree = ffmpy.FFmpeg(
            inputs={f"./public/media/_temp/{filmThree_fileName}.mp4": f"-ss 1"},
            outputs={f"./public/media/_temp/{filmThree_fileName}_Thumbnail.jpg": f"-vframes 1"}
        )
        ff_thumbnailThree.cmd
        ff_thumbnailThree.run()

        # files = ["filmOne_Clip.mp4", "filmTwo_Clip.mp4", "filmThree_Clip.mp4"]


        return Response(status=status.HTTP_201_CREATED, data={"files": [f"{filmOne_fileName}", f"{filmTwo_fileName}", f"{filmThree_fileName}"]})

        # Below is for route to make final film


class GenerateFinalFilmView(APIView):
    def post(self, request, format=None):
        request_files = json.loads(request.body)['files']
        curr_time = int(round(time.time() * 1000))
        final_file_name = f"BigSplice_{curr_time}_{randint(0,1000000)}"
        text_file = open(f'./public/media/{final_file_name}_ShotList.txt', 'w+')
        text_file.write("file BigSplice_Logo_640x480_2997.mp4\n")
        for file in request_files:
            text_file.write(f"file ./_temp/{file}.mp4\n")
        text_file.close()
        ff_merge = ffmpy.FFmpeg(
            inputs={
                f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/public/media/{final_file_name}_ShotList.txt": "-safe 0 -f concat"},
            outputs={f"./public/media/_temp/{final_file_name}.mp4": "-c copy"}
        )

        ff_merge.cmd
        ff_merge.run()

        # def clear_files(request_files):
        #     print("start of clear_files call")
        #     for file in request_files:
        #         print(f"deleting: {file}")
        #         os.remove(f"./public/media/_temp/{file}")
        #     print("request_files have been deleted")

        # timer = Timer(5.0, clear_files, [request_files])

        # timer.start()

        return Response(status=status.HTTP_201_CREATED, data={"file": f"{final_file_name}"})

class RemoveFilesView(APIView):
    def post(self, request, format=None):
        print(request)
        clips_to_delete = json.loads(request.body)['clips']
        main_to_delete = json.loads(request.body)['main']
        if len(clips_to_delete) > 0:
            for file in clips_to_delete:
                print(f"deleting: {file}")
                os.remove(f"./public/media/_temp/{file}.mp4")
                os.remove(f"./public/media/_temp/{file}_Thumbnail.jpg")
        if len(main_to_delete) > 0:
            print(f"deleting: {main_to_delete}.mp4")
            os.remove(f"./public/media/_temp/{main_to_delete}.mp4")
            os.remove(f"./public/media/{main_to_delete}_ShotList.txt")
        print("files have been deleted")
        return Response(status=status.HTTP_202_ACCEPTED, data={"clips_deleted": clips_to_delete, "main_deleted": main_to_delete})



# class AllFilmsView(generics.ListAPIView):
#     queryset = Film.objects.all()
#     serializer_class = FilmSerializer

# class RandomFilmView(generics.ListAPIView):
#     queryset = Film.random_film.get_random_film()
#     serializer_class = FilmSerializer

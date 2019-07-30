import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models import Film
from random import randint
import time
from django.conf import settings
import subprocess


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
        arr_of_films = []
        for i in range(1,4):
            film = Film.random_film.get_random_film()
            film_totalShots = len(film['timecodes'])
            film_random_idx = randint(0, film_totalShots - 3)
            film_end_tc = round(
                float(film['timecodes'][film_random_idx + randint(1, 3)]) - (2 / 29.97), 2)
            if float(film_end_tc) - float(film['timecodes'][film_random_idx]) > 60:
                film_end_tc = float(
                film['timecodes'][film_random_idx]) + 60
            elif float(film_end_tc) - float(film['timecodes'][film_random_idx]) < 5:
                film_end_tc = float(
                film['timecodes'][film_random_idx]) + 30
            film_fileName = f"Clip{i}_{film['identifier']}_{''.join(str(film['timecodes'][film_random_idx]).split('.'))}_{''.join(str(film_end_tc).split('.'))}_{randint(0, 1000000)}"
            process1 = subprocess.Popen(['ffmpeg', '-ss', f'{film["timecodes"][film_random_idx]}', '-i', f'{film["url"]}', '-t', f'{film_end_tc - float(film["timecodes"][film_random_idx])}', '-r', '30000/1001',
                                     '-vf', 'scale=640x480,setsar=1:1', '-b:v', '3M', '-maxrate', '5M', '-bufsize', '1M', '-strict', '-2', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', os.path.join(settings.MEDIA_DIR, f'{film_fileName}.mp4')])
            process1.wait()
            process2 = subprocess.Popen(['ffmpeg', '-ss', '1', '-i', f'{os.path.join(settings.MEDIA_DIR, f"{film_fileName}.mp4")}',
                                     '-vframes', '1', '-vf', 'scale=256x192,setsar=1:1', f'{os.path.join(settings.MEDIA_DIR, f"{film_fileName}_Thumbnail.jpg")}'])
            process2.wait()
            arr_of_films.append(film_fileName)

        return Response(status=status.HTTP_201_CREATED, data={"files": arr_of_films})

class GenerateFinalFilmView(APIView):
    def post(self, request, format=None):
        request_files = request.data.get('files')
        curr_time = int(round(time.time() * 1000))
        final_file_name = f"BigSplice_{curr_time}_{randint(0,1000000)}"
        text_file = open(os.path.join(settings.MEDIA_DIR,
                                      f'{final_file_name}_Shotlist.txt'), 'w+')
        text_file.write(
            f"file {os.path.join(settings.BASE_DIR, 'media', 'BigSplice_Logo_640x480_2997.mp4')}" + "\n")
        for file in request_files:
            text_file.write(
                f"file {os.path.join(settings.MEDIA_DIR, f'{file}.mp4')}" + "\n")
        text_file.write(
            f"file {os.path.join(settings.BASE_DIR, 'media', 'BigSplice_End_640x480_2997.mp4')}" + "\n")
        text_file.close()

        process = subprocess.Popen(['ffmpeg', '-safe', '0', '-f', 'concat', '-i',
                                    f'{os.path.join(settings.MEDIA_DIR, f"{final_file_name}_Shotlist.txt")}', '-c', 'copy', f'{os.path.join(settings.MEDIA_DIR, f"{final_file_name}.mp4")}'])
        process.wait()

        return Response(status=status.HTTP_201_CREATED, data={"file": f"{final_file_name}"})

class RemoveFilesView(APIView):
    def post(self, request, format=None):
        print(request)
        keys = ['clips', 'main']
        clips_to_delete, main_to_delete = [
            request.data.get(key) for key in keys]
        if len(clips_to_delete) > 0:
            for file in clips_to_delete:
                print(f"deleting: {file}")
                os.remove(os.path.join(settings.MEDIA_DIR, f'{file}.mp4'))
                os.remove(os.path.join(
                    settings.MEDIA_DIR, f'{file}_Thumbnail.jpg'))
        if len(main_to_delete) > 0:
            print(f"deleting: {main_to_delete}.mp4")
            os.remove(os.path.join(
                settings.MEDIA_DIR, f'{main_to_delete}.mp4'))
            os.remove(os.path.join(settings.MEDIA_DIR,
                                   f'{main_to_delete}_Shotlist.txt'))
        print("files have been deleted")
        return Response(status=status.HTTP_202_ACCEPTED, data={"clips_deleted": clips_to_delete, "main_deleted": main_to_delete})

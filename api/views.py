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
        # The route is currently configured to pull three clips, which are stored in a list
        for i in range(1,4):
            # Calls get_random_film method from Film Manager to get random source
            film = Film.random_film.get_random_film()
            # Total number of shots in film, based on list of timecodes in database
            film_totalShots = len(film['timecodes'])
            # Sets index at which to start clip, which should be somewhere between 0 and the third-to-last shot to account for the end of the clip
            film_random_idx = randint(0, film_totalShots - 3)
            # Defines end of clip, which will be one to three shots from the start TC. In order to not include the first frame from the following shot, the value of 2 frames at 29.97fps are subtracted
            film_end_tc = round(
                float(film['timecodes'][film_random_idx + randint(1, 3)]) - (2 / 29.97), 2)
            # If the clip duration is too long, the end point will be set to 60 seconds after the beginning
            if float(film_end_tc) - float(film['timecodes'][film_random_idx]) > 60:
                film_end_tc = float(
                film['timecodes'][film_random_idx]) + 60
            # Likewise if the clip is less than 5 seconds
            elif float(film_end_tc) - float(film['timecodes'][film_random_idx]) < 5:
                film_end_tc = float(
                film['timecodes'][film_random_idx]) + 30
            # File name should include clip number, source film name, start and end TCs, and a random ID at the end to assure no duplicate names
            film_fileName = f"Clip{i}_{film['identifier']}_{''.join(str(film['timecodes'][film_random_idx]).split('.'))}_{''.join(str(film_end_tc).split('.'))}_{randint(0, 1000000)}"
            # First process calls FFmpeg through Bash command, which takes in start time (-ss), input file (-i), duration (-t), framerate (-r; set to 29.97fps for consistency), resolution and pixel aspect ratio (-vf), and additional info for bitrates
            process1 = subprocess.Popen(['ffmpeg', '-ss', f'{film["timecodes"][film_random_idx]}', '-i', f'{film["url"]}', '-t', f'{film_end_tc - float(film["timecodes"][film_random_idx])}', '-r', '30000/1001',
                                     '-vf', 'scale=640x480,setsar=1:1', '-b:v', '3M', '-maxrate', '5M', '-bufsize', '1M', '-strict', '-2', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', os.path.join(settings.MEDIA_DIR, f'{film_fileName}.mp4')])
            process1.wait()
            # Second FFmpeg process called to create thumbnail one second into clip
            process2 = subprocess.Popen(['ffmpeg', '-ss', '1', '-i', f'{os.path.join(settings.MEDIA_DIR, f"{film_fileName}.mp4")}',
                                     '-vframes', '1', '-vf', 'scale=256x192,setsar=1:1', f'{os.path.join(settings.MEDIA_DIR, f"{film_fileName}_Thumbnail.jpg")}'])
            process2.wait()
            arr_of_films.append(film_fileName)
        # List of file names sent as response
        return Response(status=status.HTTP_201_CREATED, data={"files": arr_of_films})

class GenerateFinalFilmView(APIView):
    def post(self, request, format=None):
        # List of file names sent to view
        request_files = request.data.get('files')
        # Calculates current time to use as ID for files, to avoid potential duplicate names
        curr_time = int(round(time.time() * 1000))
        final_file_name = f"BigSplice_{curr_time}_{randint(0,1000000)}"
        # Writes text file with all of the input file names/paths, which will be read by FFmpeg. It will also include the beginning and end logos.
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
        # Runs FFmpeg with text file as input to allow for concatenation of all clips into a single file to be played
        process = subprocess.Popen(['ffmpeg', '-safe', '0', '-f', 'concat', '-i',
                                    f'{os.path.join(settings.MEDIA_DIR, f"{final_file_name}_Shotlist.txt")}', '-c', 'copy', f'{os.path.join(settings.MEDIA_DIR, f"{final_file_name}.mp4")}'])
        process.wait()
        # Returns final file name as response
        return Response(status=status.HTTP_201_CREATED, data={"file": f"{final_file_name}"})

class RemoveFilesView(APIView):
    def post(self, request, format=None):
        print(request)
        keys = ['clips', 'main']
        # Request can include clips and/or the final film to delete
        clips_to_delete, main_to_delete = [
            request.data.get(key) for key in keys]
        # Will only proceed with deleting clips if names passed in
        if len(clips_to_delete) > 0:
            for file in clips_to_delete:
                # Deletes .mp4 video files as well as .jpg thumbnail files
                print(f"deleting: {file}")
                os.remove(os.path.join(settings.MEDIA_DIR, f'{file}.mp4'))
                os.remove(os.path.join(
                    settings.MEDIA_DIR, f'{file}_Thumbnail.jpg'))
        # Will only proceed with deleting final files if name passed in
        if len(main_to_delete) > 0:
            # Deletes .mp4 video file and shotlist text file
            print(f"deleting: {main_to_delete}.mp4")
            os.remove(os.path.join(
                settings.MEDIA_DIR, f'{main_to_delete}.mp4'))
            os.remove(os.path.join(settings.MEDIA_DIR,
                                   f'{main_to_delete}_Shotlist.txt'))
        print("files have been deleted")
        return Response(status=status.HTTP_202_ACCEPTED, data={"clips_deleted": clips_to_delete, "main_deleted": main_to_delete})

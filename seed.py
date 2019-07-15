import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_big_splice.settings')

import django
django.setup()

import asyncio
from internetarchive import search_items, get_item
import json
import subprocess
import ffmpy
from api.models import Film



list_of_meta_keys = ['collection', 'description', 'identifier', 'subject', 'title']
list_of_probe_keys = ['duration', 'width', 'height', 'avg_frame_rate']


def populate():
  for i in search_items('collection:Film_Noir', list_of_meta_keys):
    collection, description, identifier, tags, title = [
        i[k] for k in list_of_meta_keys]
    item = get_item(identifier)
    file_name = next(filter(lambda x: ".mp4" in x['name'], item.files), None)[
        'name']
    url = f"https://archive.org/download/{identifier}/{file_name}"
    ff = ffmpy.FFmpeg(
        inputs={url: '-hide_banner'},
        outputs={
            "pipe:1": '-an -filter:v "select=\'gt(scene, 0.3)\', showinfo" -f null'}
    )
    ff.cmd
    _, stderr = ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    shot_log = stderr.decode("utf-8").split("\n")
    filtered_output = list(
        filter(lambda x: "Parsed_showinfo_1" in x and "pts_time" in x, shot_log))
    timecodes = list(map(lambda y: ((next(filter(lambda z: z.startswith(
        "pts_time"), y.split(" ")), None)).split(":"))[1], filtered_output))
    probe = ffmpy.FFprobe(inputs={url: None},
                          global_options=[
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format', '-show_streams'])
    stdout, _ = probe.run(stdout=subprocess.PIPE)
    probe_data = json.loads(stdout.decode('utf-8'))['streams'][0]
    duration, resolution_width, resolution_height, frame_rate = [
        probe_data[j] for j in list_of_probe_keys]
    film = Film.objects.get_or_create(collection=collection, description=description, identifier=identifier, tags=tags, title=title,
                                      file_name=file_name, url=url, timecodes=timecodes, duration=duration, resolution_width=resolution_width, resolution_height=resolution_height, frame_rate=frame_rate)[0]
    print(film)


if __name__ == '__main__':
  print('populating script')
  populate()
  print('populating complete')

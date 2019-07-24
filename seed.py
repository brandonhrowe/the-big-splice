import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_big_splice.settings')
import django
django.setup()

import asyncio
from internetarchive import search_items, get_item, configure
import json
import subprocess
import ffmpy
from api.models import Film

configure(os.environ['IA_USER'], os.environ['IA_PASSWORD'])

list_of_meta_keys = ['identifier', 'title', 'collection', 'description', 'subject']
list_of_probe_keys = ['duration', 'width', 'height', 'avg_frame_rate']


def populate():
  for i in search_items('collection:Film_Noir', list_of_meta_keys):
    if "Weirdness Bad Movie" in i['title'] or i['title'] == 'Sobaka':
        continue
    identifier = i['identifier']
    title = i['title']
    collection = i.get('collection', ['Film_Noir'])
    description = i.get('description', 'no description')
    tags = i.get('subject', [])
    if type(tags) is not list:
        tags = list(tags)
    item = get_item(identifier)
    file_name = next(filter(lambda x: ".mp4" in x['name'], item.files), None)['name']
    url = f"https://archive.org/download/{identifier}/{file_name}"

    probe = ffmpy.FFprobe(inputs={url: None},
                          global_options=[
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format', '-show_streams'])
    stdout, _ = probe.run(stdout=subprocess.PIPE)
    probe_data = json.loads(stdout.decode('utf-8'))['streams'][0]
    duration = probe_data.get('duration', 0)
    resolution_width = probe_data.get('width', 640)
    resolution_height = probe_data.get('height', 480)
    frame_rate = probe_data.get('avg_frame_rate', "30000/1001")
    if frame_rate == "0/0":
        continue

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
    # duration, resolution_width, resolution_height, frame_rate = [
    #     probe_data[j] for j in list_of_probe_keys]
    film = Film.objects.get_or_create(collection=collection, description=description, identifier=identifier, tags=tags, title=title,
                                      file_name=file_name, url=url, timecodes=timecodes, duration=duration, resolution_width=resolution_width, resolution_height=resolution_height, frame_rate=frame_rate)
    print(film)


if __name__ == '__main__':
  print('populating script')
  populate()
  print('populating complete')

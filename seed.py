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

# Allows access to Internet Archive API through key
configure(os.environ['IA_USER'], os.environ['IA_PASSWORD'])

list_of_meta_keys = ['identifier', 'title', 'collection', 'description', 'subject']
list_of_probe_keys = ['duration', 'width', 'height', 'avg_frame_rate']


def populate():
  # Finds all titles from IA API under the Film Noir collection, filtering out known unwanted files
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
    # Finds first file in list of files with ".mp4"
    file_name = next(filter(lambda x: ".mp4" in x['name'], item.files), None)['name']
    # Determines url based on ID and file name
    url = f"https://archive.org/download/{identifier}/{file_name}"
    # Runs FFprobe on file to pull metadata about the file
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
    # If frame rate is 0, there will probably be errors in encoding later on, so it will not be stored in database
    if frame_rate == "0/0":
        continue

    # Runs FFmpeg to detect shot breaks in file, which are sent out on the stderr stream
    ff = ffmpy.FFmpeg(
        inputs={url: '-hide_banner'},
        outputs={
            "pipe:1": '-an -filter:v "select=\'gt(scene, 0.3)\', showinfo" -f null'}
    )
    ff.cmd
    _, stderr = ff.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    shot_log = stderr.decode("utf-8").split("\n")
    # Filters out data to pull times
    filtered_output = list(
        filter(lambda x: "Parsed_showinfo_1" in x and "pts_time" in x, shot_log))
    # Further filtering of data to make a list
    timecodes = list(map(lambda y: ((next(filter(lambda z: z.startswith(
        "pts_time"), y.split(" ")), None)).split(":"))[1], filtered_output))
    # Creates film instance in database including all of the above data
    film = Film.objects.get_or_create(collection=collection, description=description, identifier=identifier, tags=tags, title=title,
                                      file_name=file_name, url=url, timecodes=timecodes, duration=duration, resolution_width=resolution_width, resolution_height=resolution_height, frame_rate=frame_rate)
    print(film)


if __name__ == '__main__':
  print('populating script')
  populate()
  print('populating complete')

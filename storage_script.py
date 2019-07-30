import os
import datetime

def clear_files():
    current_time = datetime.datetime.now()
    hour_ago = (current_time - datetime.timedelta(hours=1)).timestamp()
    MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', '_temp')
    with os.scandir(MEDIA_DIR) as files:
      for file in files:
          if file.name == '.gitkeep':
              continue
          elif os.path.getmtime(os.path.realpath(file)) < hour_ago:
              os.remove(os.path.realpath(file))


if __name__ == '__main__':
    clear_files()

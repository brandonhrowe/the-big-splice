# The Big Splice

www.thebigsplice.com

The Big Splice is a site for users to piece together their own mini-movie using clips from classic film noir films.


# Installation

This project was built with Django, which requires a SECRET_KEY variable in the settings.py file in order to run. Because of this, one would have to build their own Django project from scratch with its own secret key. Therefore, the below instructions are taking into account access to a Django secret key.

For recreating this app, first fork and clone the following Github repo: https://github.com/brandonhrowe/the-big-splice

The project will require all of the libraries from the requirements.txt file to be installed.

```bash
pip install -r requirements.txt
```

A Postgres database will need to be created with the name "the_big_splice"

```bash
createdb the_big_splice
```

There is a film.json file included that contains all the necessary data for the Postgres database. To migrate this data to your own database, make sure the API model has been migrated (python manage.py migrate / python manage.py makemigrations) and then run:

```bash
python manage.py loaddata film.json
```

If you wish to populate the database from scratch, it will require an account with the [Internet Archive](https://archive.org/) and have the username and password saved as environment variables ("IA_USER" and "IA_PASSWORD").

To install Internet Archive command line tool:

```bash
curl -LOs https://archive.org/download/ia-pex/ia
chmod +x ia
```

To save the config file to ~/.config/ia.ini (which is taken care of in the settings.py and seed.py):

```bash
ia configure
```

Then you can run:

```bash
python seed.py
```

Just be aware that this process will take several hours, since it has to analyze close to 100 feature-length files.

Because the frontend is built up with React, the static files first have to be generated before the app can be shown. Navigate into the the_big_splice_frontend directory and perform the following commands:

```bash
npm install
npm run build
```

The npm run build command will generate all of the static files - HTML, CSS, and JS - into a build/static folder, which is accessed when serving static assets.

### NOTE

Even though The Big Splice is currently hosted on an NGINX server, which is essential for properly serving out video media files, the current configuration is unfortunately only able to serve these files through uWSGI, which is unable to properly handle partial responses. Because of this, video playback is somewhat limited and navigation not supported at the moment. In the future I hope to migrate to a different host in order to let NGINX properly serve the media files.

# Running Locally

1. If you are using a conda environment, run that using:

```bash
source activate the-big-splice
```

Make sure the frontend is build:

```bash
cd the_big_splice_frontend
npm i
npm run build
cd ..
```

Finally, run Django:

```bash
python manage.py runserver
```

By default, you should be able to see the app on localhost:8000

# Usage

### Start

![Home](/readme/BigSplice_Home.png)

Upon loading up the site, the user has two options: "Read More" and "Start". "Read More" opens up a modal that further describes the project. "Start" will initalize the first phase of the app:

### Clips

![Loading](/readme/BigSplice_Loading.png)

Upon clicking "Start", the site will immediately start generating three random clips for the user to use. While those are generated, the user will be greeted to a Loading page.

![Clips](/readme/BigSplice_Clips.png)

As soon as all three clips are ready, the user will have access to three thumbnail images associated to those clips. The user can then drag-and-drop those thumbnails around in whatever order they wish. They can then click the "Create Your Movie" button.

### Final Film

![Movie](/readme/BigSplice_Movie.png)

When the user requests for their movie, they will be taken to the Loading page again until the file is ready. When it is, the video will appear for the user and immediately start playing. At any point, the user can return to the Clips page and either reorder the current clips into a new movie, or load new clips.


# Features

## Seed Data From Internet Archive and FFmpeg

There are several steps involved with the basic functionality of the page. Before anything, it requires a database full of information from the Internet Archive and the necessary files. The seed.py file that populates the database utilizes two libraries: internetarchive and ffmpeg.

### Internet Archive

The Internet Archive's Python library, internetarchive, allows for accessing their API. In the seed file, all of the titles and pertinent information from the Internet Archive's collection of Film Noir are called. Before any processing begins within the loop over all these titles, a few undesirable titles are filtered out.

After that, all of the potentially important pieces of data are saved in variables to eventually be able to add to the database later. (While not every field from the table is utilized in the app at the moment, I felt it important to retain data that could potentially be useful for future features.)

Finally, from the list of all files associated with each title, the script parses out the .mp4 file to know which video file to work with for the next steps.

### FFmpeg

Once the script has a reference to the URL to the proper .mp4 file for each title, the file is run through two processes with FFmpeg. The first process uses FFprobe for analyzing the technical specifications of the file (resolution, frame rate, etc.). Similar to the Internet Archive data, some of this information is not necessarily used at the moment, but is preserved for potential future features.

Next, the file is run through FFmpeg in order to analyze all of the shot changes for each film. This information is then stored as a list and saved as an array of strings in the database with the rest of the information for each title.

## Random Clip Creation

When the user clicks the "Start" button, the program will initiate the clip generation process. Similarly to how the seed file is generated, both internetarchive and FFmpeg are also incorporated into the processes of generating clips.

When the GenerateRandomClipView is called, it first calls a method on the model to pull a random title from the database table. Then, for each title, a random starting timecode is selected from the list of shot changes saved in the database. A matching end timecode is then also selected, based on a following shot change anywhere from one to three spots away (this is to assure some variety in the duration of how long each film's clip runs).

Then FFmpeg is called to encode the clips. The three essential variables are the URL for the source file, the start timecode, and the end timecode. Beyond that, a consistent bitrate, resolution, and framerate is applied to allow for easy compiling later on for the final film. The generated clips are stored in a temp folder accessible by the /media/ route.

Finally, FFmpeg is also used to create thumbnail images, also saved to the temp directory. The response to the request is the root names for the three clips to allow for both accessing the correct clips/thumbnails on the frontend as well as deleting the correct files later on.

## Rearranging Clips

Once the clips have been encoded, the user has the option of rearranging the order of the clips for how they want the shots to be cut together.

### React

The app has reference to the three clips/thumbnails the user has generated with the main React component's state. This will allow for, amongst other functions, accessing the correct thumbnails for the user to see on the frontend.

### React Sortable HOC and ArrayMove

In order to allow for the drag-and-drop functionality for the user, the library React Sortable HOC was used. In short, it serves its own React component containers for items and collection of items. This was combined with the ArrayMove library, which simplified the process of reordering the state's array of clip names.

## Final Film

Once the user has settled on an order for the clips, they can generate the final film for their viewing pleasure.

### FFmpeg

The process for generating the final film, as with the clips, utilizes FFmpeg. In order to concatenate the three clips (as well as the intro and outro logos), a .txt file is generated with file paths to all the files. FFmpeg then references that .txt file to generate a new .mp4 video file for the viewer.

### Video.JS

Once the file is ready, a Player component is rendered for the user. The Video.JS library is used to present the video window with a cleaner display than the default HTML video element. Settings are passed into the VideoJS component, including the source file directory.

## Maintaining Storage

One potential risk with writing so many files to storage - especially video files - is that space will quickly get eaten up. That's why, at every phase of the process, API routes are called to remove any files no longer needed. For example: before a call to make new clips is made, first a remove request is made for any files currently saved to this.state.

Even more important, though, is that a "beforeunload" event listener is added to the window upon the app mounting. This triggers a warning message to pop up whenever the user tried to refresh or leave the page. Once they've confirmed, the remove request is made for everything in this.state, assuring that all files from that session have been cleared from storage.

# Future Developments

### Migrate to Different NGINX host to Support Proper Video Playback

As mentioned above, even though The Big Splice is currently being served through an NGINX server, the media files are not being served directly from NGINX, causing limitations in video playback. The main change that I hope to make is to serve the site from a different server where the NGINX configuration can be modified to serve the media assets.

### Optimize for Scaling

One of the other primary issues that would have to be changed should this project grow in scale is managing the media assets. At the moment, the Django project itself is also responsible for running all of the FFmpeg processes as well. In an ideal setup, all video encoding would be allocated to its own server, separate from the main Django setup.

Additionally, all of the media creation/retrieval could be handled by a service such as AWS. This could allow for more flexibility in the number of clips created, for example, as well as using higher quality material (rather than the Standard Def material from Internet Archive).

However, the main goal of this project was to build a relatively simple venue for processing and serving video assets. In that regard, this project accomplishes its mission for the time being.

### Expanding the Number of Genres

For the initial phase of this project, I chose to limit the pool of source films to just the Internet Archive's Film Noir collection. This decision was partially to establish a specific theme for the site, and partially to make the seed data of a manageable size. Even expanding the selection to include the Internet Archive's Horror collection would be close to 500 titles, compared to less than 100 for Film Noir.

Nevertheless, because the data retrieved by the Film Noir collection proved to be consistent enough, there is a chance adding to the types of footage The Big Splice pulls from could be on the horizon...


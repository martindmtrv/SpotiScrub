# SpotiScrub

This is a python program to clean out your playlists by creating a non-explicit version of your favorite playlist!

# Required modules

Python will attempt to install these modules for you however here are the modules used in case it is not able to.

spotipy for python:
pip install spotipy

# How to use it

Step 1:

Run the program in python3 and you will be prompted to enter your username (not email address)

Step 2:

Follow the spotify signon page that will pop up!

Step 3:

After logging in DON'T CLOSE THE TAB!!

You need to copy the link it redirects you to as this will be your authorization token. Copy and paste it into the terminal and hit enter.

Step 4:

SpotiScrub will display a list of your playlists and ask you which playlist you'd like to Scrub.
Enter your selection by inputting the number that corresponds to the playlist!

Step 5:

Spotipy will do all the heavy lifting generating a new playlist with clean songs only!
Once this is complete it will prompt you again with a list of playlists;

This time select the playlist you wish to OVERWRITE, or if you'd like a fresh new playlist select 'n' (this will generate a new playlist titled SpotiScrubbed with the current date)

Step 6:

SpotiScrub will output the results of how many songs it was able to find with a percentage success rate (usually around 50-60%) depending on the playlist.

The failed attempts are due simply to there not being a clean version of that song available on Spotify.

Step 7:

You can now check spotify on whatever device you are using and you'll be able to see the new playlist and you'll notice there are no explicit tags to be seen!

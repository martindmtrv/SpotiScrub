# import regular python libraries
from datetime import date
import os

# import required modules
try:
    import spotipy
    import spotipy.util as util
# if user doesn't have them installed attempt to grab packages for them
except ImportError:
    os.system('pip3 install spotipy')
    import spotipy
    import spotipy.util as util

def auth(username):
    id = "6b4c09706f084c6bb5586a662b83f0e3" # establish user score and authetication tokens
    secret = "161ad390e0694dfe8e871e61e31079aa"
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(username,scope,client_id=id,client_secret=secret,redirect_uri='http://localhost:8888/callback/')
    sp = spotipy.Spotify(auth=token)
    return sp

# syntax for search results var['type']['items'][number in search result]['name' or 'explicit']
# explicit returns true or false; we need to find the explicit false version
# test to loop results to look for non-explicit

def findSongs(sp,username):
    print('Find songs'.center(80,'-'))
    print('Select a playlist to scrub')
    dirty = sp.user_playlist_tracks(username,showPlaylists(sp,username))
    tracks = dirty['items']
    while dirty['next']:
        dirty = sp.next(dirty)
        tracks.extend(dirty['items'])
    trackNames = [] # initialize variables
    x = 0
    for songs in tracks:    # loop through all songs in playlist and collect artist and track names to store in dictionary
        trackNames.append({"name":songs['track']['name']})
        trackNames[x]['artist'] = songs['track']['artists'][0]['name']
        trackNames[x]['album'] = songs['track']['album']['name']
        trackNames[x]['albumUri'] = songs['track']['album']['uri']
        x+=1
    return trackNames

def albumScrub(sp,query):
    results = sp.search(q="album:"+query['album'],type='album',limit=10)
    found = False
    if results['albums']['items']==[]:
        return None
    for album in results['albums']['items']:
        if album['uri']!=query['albumUri']:
            if album['name']==query['album']:
                if album['artists'][0]['name']==query['artist']:
                    break
    items = sp.album_tracks(album['uri'], limit=50, offset=0)
    trackNum = 0
    for song in items['items']:
        if song['artists'][0]['name']==query['artist']:
            if song['name'].lower()==query['name'].lower():
                if song['explicit']==False:
                    found = True
                    break
    if found:
        return song['uri']
    else:
        return None

def scrubSongs(sp,trackNames):
    cleanTrackids = []  # initialize variables
    failed = 0  # keep count of failed scrubs
    print('Scrubbing...'.center(80,' '))
    for query in trackNames:    # search each track for clean version
        results = sp.search(q="track:"+query['name'],type='track',limit=20) # look through top 30 results
        itemNum = 0
        for cleanup in results['tracks']['items']:
            if cleanup['explicit']==True:   # if explicit go to next item
                itemNum+=1
            elif cleanup['explicit']==False:    # if track is clean check if artists match
                if cleanup['artists'][0]['name']==query['artist']:
                    if cleanup['name'].lower()==query['name'].lower():
                        if cleanup['album']['name']==query['album']:
                            break
                itemNum+=1
        if itemNum>=len(results['tracks']['items']): # if failed attempt declare no clean version
            checkAlbum = albumScrub(sp,query)
            if checkAlbum!=None:
                cleanTrackids.append(albumScrub(sp,query))
            else:
                failed+=1   # keep track of failures
        else:
            cleanTrackids.append(results['tracks']['items'][itemNum]['uri']) # if succesfully found append the uri of clean song
    return cleanTrackids,failed

def showPlaylists(sp,username):
    print('\nChoose a playlist: ')
    playlists = sp.current_user_playlists()
    x = 1
    for playlist in playlists['items']:
        print('\t'+str(x)+')',playlist['name'])
        x+=1
    choice = input(' > ')
    while not choice.isnumeric() and choice!='n':
        print('Choice must be a number')
        choice = input(' > ')
    if choice=='n':
        return None
    else:
        for x in range(len(playlists['items'])):
            if int(choice)-1==x:
                return playlists['items'][x]['id']

def replaceSongs(sp,tracks,username):
    print('Replace songs'.center(80,'-'))
    print('Select a playlist to overwrite with cleaned playlist or choose \'n\' to create a new playlist with current date')
    playlist_id = showPlaylists(sp,username)
    if playlist_id==None:
        print('')
        print('Creating new playlist called SpotiScrubbed with current date'.center(80,' '),end='\n\n')
        new_playlist = sp.user_playlist_create(username, 'SpotiScrubbed '+str(date.today()), public=True)
        playlist_id = new_playlist['id']
    leftover = len(tracks)
    if leftover>=100:
        sp.user_playlist_replace_tracks(username, playlist_id, tracks[0:99])
        for x in range(1,leftover//100):
            if 99+100*x <= leftover:
                sp.user_playlist_add_tracks(username, playlist_id, tracks[100*x:99+100*x])
        if leftover-(x*100+99)!=0:
            sp.user_playlist_add_tracks(username, playlist_id, tracks[x*100+99:])
    else:
        sp.user_playlist_replace_tracks(username, playlist_id, tracks)

def welcome():
    print('Welcome to SpotiScrub'.center(80,'-'))
    print('This program will take an old spotify playlist of yours and convert your\nexplicit tracks to clean versions available on spoitfy!\nTo begin we need to authorize your spoitfy account and get a bit more info\n')
    username = input('Enter your spotify username: ')
    return username

def main(sp,username):
    trackNames = findSongs(sp,username)
    cleanTrackids,failed = scrubSongs(sp,trackNames)
    replaceSongs(sp,cleanTrackids,username)
    print(len(trackNames)-failed,"/",len(trackNames),"succesfully cleaned") # print score of completed scrubs
    print(str(int((len(trackNames)-failed)/len(trackNames)*100))+'% '+'success rate')

if __name__=="__main__":
    username = welcome()
    main(auth(username),username)

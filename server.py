from flask import Flask, render_template, request
import requests
import os
import validators
import json

fridge_host = os.getenv('FRIDGE_HOST')

# create app
app = Flask(__name__)

# define index route
@app.route('/')
def index():
    return render_template('index.html')

# define makevideo route
@app.route('/makevideo', methods=['POST'])
def makevideo():
    form = request.form
    
    song = form['song']
    background = form['background']
    reverb = form['reverb']
    speed = form['speed']
    artist = form['artist']
    title = form['title']
    title_adlib = form['title_adlib']
    twitter = form['twitter']
    soundcloud = form['soundcloud']
    spotify = form['spotify']

    # validate song
    if not validators.url(song):
        return 'invalid song (must be a url)'

    # validate background
    if not validators.url(background):
        return 'invalid background (must be a url)'

    # validate reverb
    if form['reverb'] in ['on', 'off']:
        reverb = True if reverb == 'on' else False
    else:
        return 'invald reverb value (on/off)'

    # validate speed
    try:
        speed = float(speed)
    except ValueError:
        return 'invalid speed (must be a float)'

    # validate artist
    if len(artist) < 1:
        return 'invalid artist (length must be <1)'

    # validate title
    if len(title) < 1:
        return 'invalid title (length must be <1)'

    # put all social media to one object
    social = {}

    # validate twitter
    if len(twitter) > 1:
        if not validators.url(twitter):
            return 'invalid twitter (must be a url)'
        social['twitter'] = twitter

    # validate soundcloud
    if len(twitter) > 1:
        if not validators.url(soundcloud):
            return 'invalid soundcloud (must be a url)'
        social['soundcloud'] = soundcloud

    # validate spotify
    if len(twitter) > 1:
        if not validators.url(spotify):
            return 'invalid spotify (must be a url)'
        social['spotify'] = spotify

    # create video
    video = {
        'song': song,
        'background': background,
        'reverb': reverb,
        'speed': speed,
        'artist': artist, 
        'title': title,
        'title_adlib': title_adlib,
        'social': social
    }

    # send request
    response = requests.post(fridge_host + '/freeze', data={
        'video': json.dumps(video)
    })

    return render_template('index.html', notification=response.text)

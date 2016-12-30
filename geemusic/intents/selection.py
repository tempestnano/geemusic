from flask_ask import statement, audio
from os import environ
from geemusic import ask, app, queue
from geemusic.utils.music import GMusicWrapper

@ask.intent("GeeMusicPlayArtistIntent")
def play_artist(artist_name):
    api = GMusicWrapper(environ['GOOGLE_EMAIL'], environ['GOOGLE_PASSWORD'])

    # Fetch the artist
    artist = api.get_artist(artist_name)

    # Setup the queue
    song_ids = map(lambda x: x['storeId'], artist['topTracks'])
    first_song_id = queue.reset(song_ids)

    # Get a streaming URL for the top song
    stream_url = api.get_stream_url(first_song_id)

    speech_text = "Playing top tracks from %s" % artist['name']
    return audio(speech_text).play(stream_url)

@ask.intent("GeeMusicPlayAlbumIntent")
def play_album(album_name, artist_name):
    api = GMusicWrapper(environ['GOOGLE_EMAIL'], environ['GOOGLE_PASSWORD'])

    app.logger.debug("Fetching album %s by %s" % (album_name, artist_name))

    # Fetch the album
    album = api.get_album(album_name, artist_name=artist_name)

    # Setup the queue
    song_ids = map(lambda x: x['storeId'], album['tracks'])
    first_song_id = queue.reset(song_ids)

    app.logger.debug('Queue status: %s', queue)
    app.logger.debug('Sending track id: %s', first_song_id)

    # Start streaming the first track
    stream_url = api.get_stream_url(first_song_id)

    speech_text = "Playing album %s by %s" % (album['name'], album['albumArtist'])
    return audio(speech_text).play(stream_url)

@ask.intent("GeeMusicPlaySongIntent")
def play_song(song_name, artist_name):
    api = GMusicWrapper(environ['GOOGLE_EMAIL'], environ['GOOGLE_PASSWORD'])
    queue.reset()

    app.logger.debug("Fetching song %s by %s" % (song_name, artist_name))

    # Fetch the song
    song = api.get_song(song_name, artist_name=artist_name)

    # Start streaming the first track
    stream_url = api.get_stream_url(song['storeId'])

    speech_text = "Playing song %s by %s" % (song['title'], song['artist'])
    return audio(speech_text).play(stream_url)
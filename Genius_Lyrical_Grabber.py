import requests
from rauth import OAuth2Service
import lyricsgenius
import dotenv
import os
dotenv.load_dotenv()
GeniusKey = os.environ["LGKEY"]


def test_for_number(string):
    for a in string:
        if a.isnumeric():
            return False
    return True
def remove_last_piece(string):
    for count, a in enumerate(string):
        if a.isnumeric():
            return string[:count]
    return string
def GrabLyric(SongName):    
    client = lyricsgenius.Genius(GeniusKey)
    song = client.search_song(SongName)
    lyrics = song.lyrics
    print(lyrics)
    lyrics = lyrics.splitlines(True)
    lyrics[-1] = remove_last_piece(lyrics[-1])
    lyrics[-1] = lyrics[-1].removesuffix("Embed")
    lyrics = [x for x in lyrics if test_for_number(x) or lyrics.index(x) == len(lyrics)-1]

    newlyrics = ''.join(lyrics)
    return newlyrics

if __name__ == "__main__":
    print(GrabLyric("sparks fly (taylor's version)"))
from lyricsgenius import Genius
import pandas as pd
import numpy as np
from requests.exceptions import Timeout

# Copy the key and token for the Genius API
client_id = 'jql-_AVpggl7rZfNg04BdxYXJWOeKAIkFS1D-gni59K85K2fJjP7YtCCzJoFnbQk'
client_secret = '2yZmQ-yItE-cPNIIsbISRVhIEewLUA6VlqQyl49oB9nt0Y7Wllx_mRZCYYOGTVPnxZ0G6W6_-hSnrW61VrfB0A'
token = 'eTOcesJetqOF8dStfJHAP_l5t9umjMCTgUG8Q4ULTJ7A7lhuwXpggXMUZf-FmBJf'
metadata = pd.read_excel('music_metadata pt 2.xlsx')


genius = Genius(token)
# genius.search_artist('Stevie Wonder')
# artist.save_lyrics()

lyrics = []
indices = []

# Getting the index for each song 
for i in metadata['Song Name']:
    indices.append(i)

# Getting the lyrics from the Genius API using the Artist and song name in metadata
for a, b in zip(metadata['Artist'], metadata['Song Name']):
    retries = 0
    while retries < 3:
        try:
           song = genius.search_song(a,b)
        except Timeout as e:
            retries += 1
            continue
        if song is not None:
            lyrics.append(song.lyrics)
        else:
            lyrics.append(np.NAN)
        break

# metadata['Lyrics'] = lyrics2
metadata.to_excel('music_metadata pt 2.xlsx', index=False)

# metadata = metadata.reset_index()
# indices = pd.Series(metadata.index, index=metadata['Song Name'])

# Songs/artists in different languages had to get separated and translated before using the Genius API
metadata.index = indices
metadata.loc['Subete ga F ni Naru Ed Nana Hitsuji', 'Lyrics'] = genius.search_song('Scenario Art', 'seven sheep')



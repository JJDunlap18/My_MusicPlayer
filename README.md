# Recommending Music Player: Project Overview
- Created a Music Player for my first project to test my python skills and ability to think like a programmer. As my understanding and comfortability with python advanced so did the complexity of the music player. Additional features may be added as my programming abilities progresses
- After gaining experience in Data Science, I decided to build upon this project by adding a Recommendation System based on Natural Language Processing. After extracting and storing the metadata from each song, the playlist is then organized by either similarity in the lyrics, or by artist and genre with the selected song.
- 244 songs from various artists and genres were used to test the recommendation features of the Music Player, with a similarity score being outputted so the user can compare the similarities between different songs

## Main Python Packages and Tools Used
- Pycharm
- tkinter (GUI)
- pygame (primary music player functions such as pause, play, stop and skip)
- scikit-learn (calculating Term Frequency-Inverse Document Frequence and cosine similarity for recommender system)
- pandas (storing metadata in an excel format)
- tinytag (extracting metadata from songs)
- mutagen (manipulating .mp3 and .wav files)
- Genius API (get lyrics for most songs)

## Music Player Interface and Features

![Music Player](https://user-images.githubusercontent.com/74473048/156452417-9f2934b8-7af6-40c2-911d-0c5746b60d7b.JPG)

The image above shows the music player interface with its different features. The main features I want to highlight are the following:
- The sliding bar below the song title that can be dragged to change the position within the song
- The ABC icon that will calculate the similarity score between each song and the highlighted song then reorganize the playlist in descending order of similarity scores
- The crossing arrows icon that will shuffle the song order
- The person icon that will do the same as the ABC icon but but will base the order by artist and genre
- Below is a portion of the list that shows the similarity scores in respect to the highlighted song and the reorganized list:

![Music Player 2](https://user-images.githubusercontent.com/74473048/156454290-f0ea47d7-541d-4390-acce-c2c05646fe31.JPG)

![Similarity Scores](https://user-images.githubusercontent.com/74473048/156454526-2034bcb6-9316-4623-ab02-3e52aaaff5df.JPG)


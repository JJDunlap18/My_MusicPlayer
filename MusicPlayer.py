from tkinter import *
from pygame import mixer
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import tkinter.ttk as ttk
import random
from tinytag import TinyTag
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity


class MusicPlayer:

    def __init__(self):

        # Creating the root window for the music player
        root = Tk()
        root.geometry('585x390')
        root.resizable(True, False)  # Prevents the music player window from being resized
        root.title('JD Music Player')

        # Initialize the pygame mixer module
        mixer.init()

        # Creating the main frame for the music player
        player_frame = Frame(root)
        player_frame.pack()

        # Creating a scroll bar for the playlist
        scroll_bar = Scrollbar(player_frame, orient=VERTICAL)

        # Creating the directory for the songs
        self.song_playlist = Listbox(player_frame, bg='white', fg='black', width=70, selectbackground='gray', selectforeground='black', yscrollcommand=scroll_bar.set)
        self.song_playlist.grid(row=0, column=0, pady=10)

        # Adding the scroll bar to player_frame
        scroll_bar.config(command=self.song_playlist.yview)  # configures the scroll bar to be viewed vertically
        scroll_bar.grid(row=0, column=1, sticky=N+S)  # sticky N+S stretches the scroll bar vertically

        # Creating the main menu on the root window
        song_menu = Menu(root)
        root.config(menu=song_menu)  # updates the root window to have a menu option

        # Creating a menu for adding songs to the playlist
        add_song_menu = Menu(song_menu)
        song_menu.add_cascade(label='Add Songs', menu=add_song_menu)  # adds a menu called 'Add Songs' to the root window
        add_song_menu.add_command(label='Add Songs to Playlist', command=self.add_songs)  # creates an option to add songs under the 'Add Songs' menu

        # Creating a menu for removing songs from the playlist
        remove_song_menu = Menu(root)
        song_menu.add_cascade(label='Remove Songs', menu=remove_song_menu)  # adds a menu called 'Remove Songs' to the root window
        remove_song_menu.add_command(label='Remove Song from Playlist', command=self.remove_song)  # removes the selected song from the playlist
        remove_song_menu.add_command(label='Remove All Songs from Playlist', command=self.remove_all_songs)  # removes all songs from the playlist

        # Creating the current song display and sliding bar that moves along with the song
        slider_frame = Frame(player_frame)
        slider_frame.grid(row=1, column=0, pady=10)
        self.start_time = Label(slider_frame, text='', bd=1)
        self.end_time = Label(slider_frame, text='', bd=1)
        self.song_display = Label(slider_frame, text='')

        self.my_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=self.slider, length=375)
        self.my_slider.grid(row=1, column=1)
        self.start_time.grid(row=1, column=0, padx=5)
        self.end_time.grid(row=1, column=2, padx=5)
        self.song_display.grid(row=0, column=1)

        # Creating the frame for the buttons
        controls_frame = Frame(player_frame)
        controls_frame.grid(row=2, column=0, pady=5)

        # Images for the play, stop, pause, rewind, and forward buttons
        back_img = PhotoImage(file='Button_Images/backward.png')
        forward_img = PhotoImage(file='Button_Images/forward.png')
        play_img = PhotoImage(file='Button_Images/play.png')
        pause_img = PhotoImage(file='Button_Images/pause.png')
        stop_img = PhotoImage(file='Button_Images/stop.png')
        shuffle_img = PhotoImage(file='Button_Images/shuffle.png')
        lyric_img = PhotoImage(file='Button_Images/lyrics.png')
        artist_img = PhotoImage(file='Button_Images/artist.png')

        # Creating buttons for the player
        play_button = Button(controls_frame, image=play_img, borderwidth=0, command=self.play_music)
        stop_button = Button(controls_frame, image=stop_img, borderwidth=0, command=self.stop_music)
        pause_button = Button(controls_frame, image=pause_img, borderwidth=0, command=self.pause_music)
        back_button = Button(controls_frame, image=back_img, borderwidth=0, command=self.back_music)
        forward_button = Button(controls_frame, image=forward_img, borderwidth=0, command=self.next_song)
        shuffle_button = Button(controls_frame, image=shuffle_img, borderwidth=0, command=self.shuffle)
        lyrics_rec_button = Button(controls_frame, image=lyric_img, borderwidth=0, command=self.get_lyrics_recommendations)
        artist_rec_button = Button(controls_frame, image=artist_img, borderwidth=0, command=self.get_artist_and_genre_recommendation)

        # Placing buttons on the controls_frame
        back_button.grid(row=0, column=0, padx=5)
        forward_button.grid(row=0, column=1, padx=5)
        play_button.grid(row=0, column=2, padx=5)
        pause_button.grid(row=0, column=3, padx=5)
        stop_button.grid(row=0, column=4, padx=5)
        shuffle_button.grid(row=1, column=2, pady=5)
        lyrics_rec_button.grid(row=1, column=1, pady=5)
        artist_rec_button.grid(row=1, column=3, pady=5)

        # Creating the frame for the volume slider
        volume_frame = LabelFrame(player_frame, text="Volume")
        volume_frame.grid(row=0, column=2, padx=10)

        # Creating the volume slider
        self.volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=self.volume)
        self.volume_slider.pack(pady=5)

        # Displaying the current volume level
        self.volume_label = Label(volume_frame, text='')
        self.volume_label.pack()

        self.stop_playing = True  # used to track when the music player has been stopped, set to True by default so the random button can't be used immediately
        self.pause_state = False  # used to track when the song is in a paused or un-paused state
        self.play_time_var = False  # used to track when play_time is running to prevent it from running multiple times
        self.song_length = None  # used to track the length of each song for the status bar
        self.songArtists = []  # used to store the artist for each song
        self.songGenres = []  # used to store the genre for each song
        self.songTitles = []  # used to store the Title for each song
        self.songPath = []  # used to store the path for each song
        self.songFrame = None  # the dataframe containing the artist, genre, title, and path for each song
        self.elist = []  # used to check if a song already exists within the dataframe to avoid duplicates
        self.frameIndex = []

        root.mainloop()

    def get_lyrics_recommendations(self):
        song = self.song_playlist.get(ACTIVE)
        songframe = self.songFrame
        songframe = songframe.reset_index()

        # Converts Lyrics to a string
        songframe['Lyrics'] = songframe['Lyrics'].astype(str)
        # Replaces all NaN values with an empty string
        songframe['Lyrics'] = songframe['Lyrics'].fillna('')

        # Define a TF-IDF Vectorizer Object, removes all english stop words
        tfidf = TfidfVectorizer(stop_words='english')
        # Creates a TF-IDF matrix by fitting and transforming the data
        tfidf_matrix = tfidf.fit_transform(songframe['Lyrics'])
        # Calculates the numeric quantity that denotes the similarity between two songs
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        indices = pd.Series(songframe.index, index=songframe['Song Name'])

        # Gets the index of the song that matches the song name
        idx = indices[song]

        # Get the pairwise similarity scores of all songs with that song
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Sort the songs based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Return the 30 most similar scores
        sim_scores = sim_scores[1:31]
        self.stop_music()
        self.song_playlist.delete(0, END)
        song_indices = [i[0] for i in sim_scores]

        for name in song_indices:
            self.song_playlist.insert(END, songframe['Song Name'].loc[name])  # inserts each song at the end of the playlist

    def get_artist_and_genre_recommendation(self):
        song = self.song_playlist.get(ACTIVE)
        songframe = self.songFrame
        songframe = songframe.reset_index()
        features = ['Artist', 'Genre']

        for feature in features:
            songframe[feature] = songframe[feature].apply(self.clean_data)

        songframe['soup'] = songframe.apply(self.create_soup, axis=1)

        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(songframe['soup'])

        cosine_sim = cosine_similarity(count_matrix, count_matrix)

        songframe = songframe.reset_index()
        indices = pd.Series(songframe.index, index=songframe['Song Name'])

        # Gets the index of the song that matches the song name
        idx = indices[song]

        # Get the pairwise similarity scores of all songs with that song
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Sort the songs based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Return the 30 most similar scores
        sim_scores = sim_scores[1:31]
        self.stop_music()
        self.song_playlist.delete(0, END)
        song_indices = [i[0] for i in sim_scores]

        for name in song_indices:
            self.song_playlist.insert(END, songframe['Song Name'].loc[name])  # inserts each song at the end of the playlist

    def clean_data(self, frame):
        if isinstance(frame, str):
            return str.lower(frame.replace(' ', ''))
        else:
            return ''

    def create_soup(self, frame):
        return ''.join(frame['Artist']) + ' ' + ''.join(frame['Genre'])

    def check_for_csv(self):
        # path = os.walk('C:/Users/jjdun/Documents/Data Science Projects')
        file = 'C:/Users/jjdun/Documents/Data Science Projects/music_metadata.xlsx'

        if os.path.exists('C:/Users/jjdun/Documents/Data Science Projects/music_metadata.xlsx'):  # if the file exists in the given location, open that file and save it as a dataframe
            self.songFrame = pd.read_excel(file)
            # put conditional to check if songs in songframe already
            for i in self.songFrame['Song Name']:
                self.frameIndex.append(i)

            self.songFrame.index = [self.frameIndex]
            print(self.songFrame.shape)
            print(self.frameIndex)
            for i in self.songFrame.loc[self.frameIndex, 'File Path']:
                self.elist.append(i)
        else:  # else, create an empty dataframe with the given column names
            self.songFrame = pd.DataFrame(columns=['Song Name', 'Artist', 'Genre', 'File Path', 'Play Count', 'Lyrics'])
            print(self.songFrame.shape)

    def update_csv(self):
        self.songFrame.to_excel('C:/Users/jjdun/Documents/Data Science Projects/music_metadata.xlsx', index=False)

    def get_metadata(self, songs):
        # Load and grab the metadata for each song in the playlist

        for song in songs:  # Loops through each song in the playlist and adds the data to the corresponding list
            if song in self.elist:  # checks to see if the song already exists within the dataframe
                continue  # if it does exist, skip to the next song

            # self.elist.append(song)
            # Append the metadata for each song to the corresponding variable
            self.songPath.append(song)
            self.elist.append(song)
            data = TinyTag.get(song)
            self.songArtists.append(data.artist)
            self.songGenres.append(data.genre)
            # Removes the file path for each song before it is displayed in the playlist
            song = song.replace('C:/Users/jjdun/Documents/Music for Recommendation/MP3s/', '')
            self.songTitles.append(song)
            # print(self.songTitles)
        # Consolidate the above lists into a dictionary
        songDict = {'Song Name': self.songTitles, 'Artist': self.songArtists, 'Genre': self.songGenres,
                    'File Path': self.songPath, 'Play Count': 0, 'Lyrics': ''}

        # print(songDict)
        # Turn that dictionary into a pandas dataframe
        songDict = pd.DataFrame(songDict, index=self.songTitles)
        # Add the song to the existing songFrame assuming it does not already exist within the dataframe
        self.songFrame = self.songFrame.append(songDict, ignore_index=False)
        # print(self.songFrame.head(8))
        self.songArtists = []
        self.songGenres = []
        self.songTitles = []
        self.songPath = []

        self.songFrame = self.songFrame.convert_dtypes()
        # print(self.songFrame.shape)

    def update_play_count(self, song):
        # Updates the play count in the dataframe each time a song is played
        song = song.replace('C:/Users/jjdun/Documents/Music for Recommendation/MP3s/', '')
        self.songFrame.loc[song, 'Play Count'] += 1
        print(self.songFrame['Play Count'])

    def add_songs(self):
        songs = filedialog.askopenfilenames(initialdir='C:/Users/jjdun/Documents/Music for Recommendation/MP3s', title='Choose a Song', filetypes=(('mp3 files', '*.mp3'), ('wav files', '*.wav')))  # these songs are stored in a tuple
        if len(self.frameIndex) == 0:
            self.check_for_csv()
        self.get_metadata(songs)
        # print(self.songFrame)

        # Removing the file path for each song before it is displayed in the playlist
        for song in songs:
            song = song.replace('C:/Users/jjdun/Documents/Music for Recommendation/MP3s/', '')  # this only works if the file path is the same every time, might consider a regular expression for more global uses
            self.song_playlist.insert(END, song)  # inserts each song at the end of the playlist

    def remove_song(self):
        # consider adding: when song is deleted, highlight the next song to play and put it at the start of this function
        self.stop_music()
        self.song_playlist.delete(ANCHOR)  # removes the currently selected song from the playlist (if a song is selected, that song is considered anchored)

    def remove_all_songs(self):
        self.stop_music()
        self.song_playlist.delete(0, END)  # removes the currently selected song from the playlist (if a song is selected, that song is considered anchored)

    def play_time(self):

        # Getting how long the current song has been playing for
        current_time = mixer.music.get_pos()/1000  # gets how long the current song has been playing for (in milliseconds)

        # Grabbing the current song
        song = self.song_playlist.get(ACTIVE)  # ACTIVE here refers to what is highlighted in the playlist
        self.song_display.config(text=song, font=('Arial', 11))  # displays the current song above the slider
        song = f'C:/Users/jjdun/Documents/Music for Recommendation/MP3s/{song}'

        # Updating the playlist to scroll to the current song
        x = self.song_playlist.curselection()  # grabs the index of the current song
        if self.pause_state or self.stop_playing:
            pass
        else:
            self.song_playlist.see(x)  # scrolls to the index of the current song

        # Getting the length of each song
        if '.mp3' in song:
            song_duration = MP3(song)
        elif '.wav' in song:
            song_duration = WAVE(song)

        self.song_length = song_duration.info.length  # gets the length of the current song (in seconds)
        converted_song_length = time.strftime('%M:%S', time.gmtime(int(self.song_length)))  # converts the song length to 00:00 format

        # Tracking to see if the position of the slider has been dragged
        current_time += 1  # adds 1 to current time since the slider is one second behind the song playing
        # print(int(self.my_slider.get()), int(current_time))
        if int(self.my_slider.get() == int(self.song_length)):  # this makes sure start_time properly shows the end of the song when it matches the same time as the song length
            self.start_time.config(text=f'{converted_song_length}')
            self.end_time.config(text=f'{converted_song_length}')
            self.next_song()  # play the next song after the start time and end_time are the same
        elif self.pause_state:  # if play_state is True, do not run the rest of this if statement so it so the bar doesn't move when the song is paused
            pass
        elif int(self.my_slider.get()) == int(current_time):  # the slider is moving along with the song, the position of the slider has not been dragged yet
            slider_position = int(self.song_length)
            self.my_slider.config(to=slider_position, value=int(current_time))  # the length of the slider bar will change to the length of the song
        else:  # if the slider has been dragged, change the current time of the song to the newly dragged position of the slider
            slider_position = int(self.song_length)
            self.my_slider.config(to=slider_position, value=int(self.my_slider.get()))  # the length of the slider bar will change to the length of the song
            new_time = time.strftime('%M:%S', time.gmtime(int(self.my_slider.get())))  # changes the current time of the song to the current position of the slider
            self.start_time.config(text=f'{new_time}')  # display the new position of the slider as the current time of the song
            self.end_time.config(text=f'{converted_song_length}')
            next_time = int(self.my_slider.get()) + 1  # convert the current position of the slider to an integer (status bars are initially floats)
            self.my_slider.config(value=next_time)  # change the current value of the slider to the newly dragged position

        # Run the play_time function every second to move the slider with the song
        self.start_time.after(1000, self.play_time)

        self.play_time_var = True  # prevents play_time from running more than once, causing the slider to skip by 2 seconds instead of 1

    def play_music(self):
        # Turn stop_playing back to False so the shuffle button can be used
        self.stop_playing = False

        # Make sure the song is considered un-paused and play_state is turned False
        mixer.music.unpause()
        self.pause_state = False

        song = self.song_playlist.get(ACTIVE)  # grabs the currently selected song from the playlist

        song = f'C:/Users/jjdun/Documents/Music for Recommendation/MP3s/{song}'
        mixer.music.load(song)  # loads selected song to be played
        mixer.music.play()  # plays the currently loaded song
        self.update_play_count(song)
        self.update_csv()

        # Makes sure not to run play time if there is already an instance running
        if self.play_time_var:
            self.my_slider.config(value=0)
            self.play_time_var = False
        else:
            self.play_time()

    def stop_music(self):
        # Prevent shuffle from being used while player is stopped
        self.stop_playing = True

        # Make sure the song is considered un-paused and play_state is turned False
        mixer.music.unpause()
        self.pause_state = False

        # Reset the slider and status bar
        self.my_slider.config(value=0)
        self.start_time.config(text='')
        self.end_time.config(text='')

        mixer.music.stop()  # stops playing the current song
        self.song_playlist.selection_clear(ACTIVE)  # unselects the current selected song from the playlist
        self.song_display.config(text='')

    def pause_music(self):
        if not self.pause_state:  # if play_state is false, pause the selected song and switch it to True
            mixer.music.pause()
            self.pause_state = True
        else:  # if play_state is True, unpause the selected song and switch it back to False
            mixer.music.unpause()
            self.pause_state = False

    def back_music(self):

        # Make sure the song is considered un-paused and play_state is turned False
        mixer.music.unpause()
        self.pause_state = False

        # Reset the slider and status bar
        self.my_slider.config(value=0)

        next = self.song_playlist.curselection()  # returns the index of the currently selected song as a tuple

        if next[0] == 0:  # if next has an index of 0, skip to the last song of the playlist
            next = END

        else:  # otherwise subtract 1 from the current index and get the song at that index
            next = next[0] - 1

        # Prevents the song path from being added 2x due to the shuffle function
        song = self.song_playlist.get(next)
        if 'C:/Users/jjdun/Documents/Music for Recommendation/MP3s/' in song:
            mixer.music.load(song)
        else:
            song = f'C:/Users/jjdun/Documents/Music for Recommendation/MP3s/{song}'  # adding the file path back to the song
            mixer.music.load(song)
        mixer.music.play()
        self.update_play_count(song)

        self.song_playlist.selection_clear(0, END)  # clears the active cursor in the playlist (the 0, END means clear any selected bar from the 1st song to the last song)
        self.song_playlist.activate(next)  # highlights the currently playing song
        self.song_playlist.select_set(next, last=None)  # sets the active bar to the previous song

    def next_song(self):

        # Make sure the song is considered un-paused and play_state is turned False
        mixer.music.unpause()
        self.pause_state = False

        # Reset the slider and status bar
        self.my_slider.config(value=0)

        next = self.song_playlist.curselection()  # returns the index of the currently selected song as a tuple, this might also help with the random function (tkinter function)
        end_position = self.song_playlist.index(END)  # gets the index of the last song in the playlist

        if next[0] == end_position - 1:  # if next is the last index of the playlist, skip to the first song (had to subtract one since .index() does not start count at 0)
            next = 0

        else:  # otherwise add 1 from the current index and get the song at that index
            next = next[0] + 1

        # Prevents the song path from being added 2x due to the shuffle function
        song = self.song_playlist.get(next)
        if 'C:/Users/jjdun/Documents/Music for Recommendation/MP3s/' in song:
            mixer.music.load(song)
        else:
            song = f'C:/Users/jjdun/Documents/Music for Recommendation/MP3s/{song}'  # adding the file path back to the song
            mixer.music.load(song)

        mixer.music.play()
        self.update_play_count(song)

        self.song_playlist.selection_clear(0, END)  # clears the active cursor in the playlist (the 0, END means clear any selected bar from the 1st song to the last song)
        self.song_playlist.activate(next)  # highlights the currently playing song
        self.song_playlist.select_set(next, last=None)  # sets the active bar to the previous song

    def slider(self, x):
        # Make sure the song is considered un-paused and play_state is turned False
        mixer.music.unpause()
        self.pause_state = False

        song = self.song_playlist.get(ACTIVE)  # gets the currently playing song
        song = f'C:/Users/jjdun/Documents/Music for Recommendation/MP3s/{song}'  # adding the file path back to the song

        mixer.music.load(song)
        mixer.music.play(loops=0, start=int(self.my_slider.get()))  # starts playing the song at the current position of the slider
        self.play_time_var = False

    def volume(self, x):
        mixer.music.set_volume(self.volume_slider.get())  # sets the volume to the current value of the volume slider
        vol = mixer.music.get_volume() * 100  # gets the current volume level
        self.volume_label.config(text=int(vol))  # displays the current volume level

    def shuffle(self):
        # Make sure not to run shuffle if the music player has been stopped
        if self.stop_playing:
            return

        # Make sure the song is considered un-paused and play_state is turned False
        mixer.music.unpause()
        self.pause_state = False

        # Creating a list of randomized indices
        playlist_length = self.song_playlist.index(END)  # gets the index of the last song in the playlist
        random_playlist = list(range(0, playlist_length))  # creates a list fom 0 to the last index of the playlist
        random.shuffle(random_playlist)  # randomizes the list of indices

        num_list = len(random_playlist) - 1  # since lists start at 0, subtract 1 so the right amount of songs get deleted later in the code

        # Loop through indices, and grab each song associate with that index
        for index in random_playlist:  # for each index in random_playlist
            song = self.song_playlist.get(index)  # get the song associated with that index
            self.song_playlist.insert(END, song)

        # Delete the previous order of songs
        self.song_playlist.delete(0, num_list)  # deletes the old playlist of songs to prevent duplicates

        # Get the song in the 0 index and play it after the randomized playlist is created
        next_song = self.song_playlist.get(0)
        next_song = f'C:/Users/jjdun/Documents/Music for Recommendation/MP3s/{next_song}'
        self.my_slider.config(value=0)  # resets the slider position back to zero
        mixer.music.load(next_song)
        mixer.music.play()
        self.update_play_count(song)

        self.song_playlist.selection_clear(0, END)  # clears the active cursor in the playlist (the 0, END means clear any selected bar from the 1st song to the last song)

        self.song_playlist.activate(0)  # highlights the currently playing song
        self.song_playlist.select_set(0, last=None)  # sets the active bar to the previous song


MusicPlayer()

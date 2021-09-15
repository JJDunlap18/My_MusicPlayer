from tkinter import *
from pygame import mixer
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import tkinter.ttk as ttk


class MusicPlayer:

    def __init__(self):

        # Creating the root window for the music player
        root = Tk()
        root.geometry('540x450')
        root.resizable(False, False)  # Prevents the music player window from being resized
        root.title('JD Music Player')

        # Initialize the pygame mixer module
        mixer.init()

        # Creating the main frame for the music player
        player_frame = Frame(root)
        player_frame.pack()

        # Creating the directory for the songs
        self.song_playlist = Listbox(player_frame, bg='white', fg='black', width=80, selectbackground='gray', selectforeground='black')
        self.song_playlist.grid(row=0, column=0)

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

        # Creating the frame for the buttons
        controls_frame = Frame(player_frame)
        controls_frame.grid(row=2, column=0, pady=10)

        # Images for the play, stop, pause, rewind, and forward buttons
        back_img = PhotoImage(file='Button_Images/backward.png')
        forward_img = PhotoImage(file='Button_Images/forward.png')
        play_img = PhotoImage(file='Button_Images/play.png')
        pause_img = PhotoImage(file='Button_Images/pause.png')
        stop_img = PhotoImage(file='Button_Images/stop.png')

        # Creating buttons for the player
        play_button = Button(controls_frame, image=play_img, borderwidth=0, command=self.play_music)
        stop_button = Button(controls_frame, image=stop_img, borderwidth=0, command=self.stop_music)
        pause_button = Button(controls_frame, image=pause_img, borderwidth=0, command=self.pause_music)
        back_button = Button(controls_frame, image=back_img, borderwidth=0, command=self.back_music)
        forward_button = Button(controls_frame, image=forward_img, borderwidth=0, command=self.next_song)

        # Placing buttons on the controls_frame
        back_button.grid(row=0, column=0, padx=5)
        forward_button.grid(row=0, column=1, padx=5)
        play_button.grid(row=0, column=2, padx=5)
        pause_button.grid(row=0, column=3, padx=5)
        stop_button.grid(row=0, column=4, padx=5)

        self.stop_playing = False  # used to track when the status bar for the songs should stop updating
        self.play_state = False  # used to track when the song is in a paused or un-paused state
        self.play_time_var = False  # used to track when play_time is running so play_time2 can start
        self.song_length = None  # used to track the length of each song for the status bar

        root.mainloop()

    def add_songs(self):
        songs = filedialog.askopenfilenames(initialdir='C:/Users/jjdun/Music/Music', title='Choose a Song', filetypes=(('mp3 files', '*.mp3'), ('wav files', '*.wav')))  # these songs are stored in a tuple

        # Removing the file path for each song before it is displayed in the playlist
        for song in songs:
            song = song.replace('C:/Users/jjdun/Music/Music/', '')  # this only works if the file path is the same every time, might consider a regular expression for more global uses
            self.song_playlist.insert(END, song)  # inserts each song at the end of the playlist

    def remove_song(self):
        pass

    def remove_all_songs(self):
        pass

    def play_time(self):
        pass

    def play_time2(self):
        pass

    def play_music(self):
        song = self.song_playlist.get(ACTIVE)  # grabs the currently selected song from the playlist
        song = f'C:/Users/jjdun/Music/Music/{song}'  # adds the file path that was removed in the add_songs function so music.load() can find the song's path
        mixer.music.load(song)  # loads selected song to be played
        mixer.music.play()  # plays the currently loaded song

    def stop_music(self):
        mixer.music.stop()  # stops playing the current song
        self.song_playlist.selection_clear(ACTIVE)  # unselects the current selected song from the playlist


    def pause_music(self):
        if not self.play_state:  # if play_state is false, pause the selected song and switch it to True
            mixer.music.pause()
            self.play_state = True
        else:  # if play_state is True, unpause the selected song and switch it back to False
            mixer.music.unpause()
            self.play_state = False

    def back_music(self):
        next = self.song_playlist.curselection()  # returns the index of the currently selected song as a tuple, this might also help with the random function (tkinter function)

        if next[0] == 0:  # if next has an index of 0, skip to the last song of the playlist
            next = END

        else:  # otherwise subtract 1 from the current index and get the song at that index
            next = next[0] - 1

        song = self.song_playlist.get(next)
        song = f'C:/Users/jjdun/Music/Music/{song}'  # adding the file path back to the song
        mixer.music.load(song)
        mixer.music.play()

        self.song_playlist.selection_clear(0, END)  # clears the active cursor in the playlist (the 0, END means clear any selected bar from the 1st song to the last song)
        self.song_playlist.activate(next)  # highlights the currently playing song
        self.song_playlist.select_set(next, last=None)  # sets the active bar to the previous song


    def next_song(self):
        next = self.song_playlist.curselection()  # returns the index of the currently selected song as a tuple, this might also help with the random function (tkinter function)
        end_position = self.song_playlist.index(END)  # gets the index of the last song in the playlist

        if next[0] == end_position - 1:  # if next is the last index of the playlist, skip to the first song (had to subtract one since .index() does not start count at 0)
            next = 0

        else:  # otherwise add 1 from the current index and get the song at that index
            next = next[0] + 1

        song = self.song_playlist.get(next)
        song = f'C:/Users/jjdun/Music/Music/{song}'  # adding the file path back to the song
        # print(song)
        mixer.music.load(song)
        mixer.music.play()

        self.song_playlist.selection_clear(0, END)  # clears the active cursor in the playlist (the 0, END means clear any selected bar from the 1st song to the last song)
        self.song_playlist.activate(next)  # highlights the currently playing song
        self.song_playlist.select_set(next, last=None)  # sets the active bar to the previous song

    def shuffle(self):
        # see if song_playlist can be printed after pressing play to see if it returns a list or tuple
        # that tuple can then be randomized
        pass


MusicPlayer()

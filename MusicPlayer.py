from tkinter import *
from pygame import mixer
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import tkinter.ttk as ttk


class MusicPlayer:

    def __init__(self):

        # Creating the initial window for the music player
        root = Tk()
        root.geometry('540x450')
        root.resizable(False, False)
        root.title('JD Music Player')

        # Creating the main frame for the music player
        player_frame = Frame(root)
        player_frame.pack()

        # Creating the directory for the songs
        song_playlist = Listbox(player_frame, bg='white', fg='black', width=80, selectbackground='blue', selectforeground='black')
        song_playlist.grid(row=0, column=0)

        # Creating the menu/options for adding and removing songs from the playlist
        add_song_menu = Menu(root)
        root.config(menu=add_song_menu)  # updates the root window to have a menu option
        add_song_menu.add_cascade(label='Add Songs')  # adds a menu called 'Add Songs' to the root window
        add_song_menu.add_command(label='Add Songs to Playlist', command=self.add_songs)  # creates an option to add songs under the 'Add Songs' menu



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
        pass

    def remove_song(self):
        pass

    def remove_all_songs(self):
        pass

    def play_time(self):
        pass

    def play_time2(self):
        pass

    def play_music(self):
       pass

    def stop_music(self):
        pass

    def pause_music(self):
        pass

    def back_music(self):
        pass

    def next_song(self):
        pass


MusicPlayer()

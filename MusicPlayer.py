from tkinter import *
from pygame import mixer
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import tkinter.ttk as ttk


class MusicPlayer:

    def __init__(self):
        # if there is only one song, next and back button doesnt do anything.

        # when slider is dragged, slider moves at double speed


        # Creating the root window for the music player
        root = Tk()
        root.geometry('550x390')
        root.resizable(True, False)  # Prevents the music player window from being resized
        root.title('JD Music Player')

        # Initialize the pygame mixer module
        mixer.init()

        # Creating the main frame for the music player
        player_frame = Frame(root)
        player_frame.pack()

        # Creating the directory for the songs
        self.song_playlist = Listbox(player_frame, bg='white', fg='black', width=70, selectbackground='gray', selectforeground='black')
        self.song_playlist.grid(row=0, column=0, pady=10)

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

        self.my_slider = ttk.Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=self.slider, length=375)
        self.my_slider.grid(row=1, column=1)
        self.start_time.grid(row=1, column=0, padx=10)
        self.end_time.grid(row=1, column=2, padx=10)
        self.song_display = Label(slider_frame, text='')
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

        # Creating the frame for the volume slider
        volume_frame = LabelFrame(player_frame, text="Volume")
        volume_frame.grid(row=0, column=1, padx=3)

        # Creating the volume slider
        self.volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=self.volume)
        self.volume_slider.pack(pady=5)

        # Displaying the current volume level
        self.volume_label = Label(volume_frame, text='')
        self.volume_label.pack()

        self.stop_playing = False  # used to track when the status bar for the songs should stop updating
        self.pause_state = False  # used to track when the song is in a paused or un-paused state
        self.play_time_var = False  # used to track when play_time is running so play_time2 can start
        self.song_length = None  # used to track the length of each song for the status bar
        # self.stopped = False
        # self.slider_label = Label(root, text='0')
        # self.slider_label.pack(pady=10)

        root.mainloop()

    def add_songs(self):
        songs = filedialog.askopenfilenames(initialdir='C:/Users/jjdun/Music/Music', title='Choose a Song', filetypes=(('mp3 files', '*.mp3'), ('wav files', '*.wav')))  # these songs are stored in a tuple

        # Removing the file path for each song before it is displayed in the playlist
        for song in songs:
            song = song.replace('C:/Users/jjdun/Music/Music/', '')  # this only works if the file path is the same every time, might consider a regular expression for more global uses
            self.song_playlist.insert(END, song)  # inserts each song at the end of the playlist

    def remove_song(self):
        # consider adding: when song is deleted, highlight the next song to play and put it at the start of this function
        self.stop_music()
        self.song_playlist.delete(ANCHOR)  # removes the currently selected song from the playlist (if a song is selected, that song is considered anchored)


    def remove_all_songs(self):
        self.stop_music()
        self.song_playlist.delete(0, END)  # removes the currently selected song from the playlist (if a song is selected, that song is considered anchored)

    def play_time(self):

        # if self.play_time_var:
        #     return

        # Getting how long the current song has been playing for
        current_time = mixer.music.get_pos()/1000  # gets how long the current song has been playing for (in milliseconds)
        # self.slider_label.config(text=f'Slider: {int(self.my_slider.get())} and Song pos: {int(current_time)}')
        # new_time = time.strftime('%M:%S', time.gmtime(current_time))  # formats the time from current_time

        # Grabbing the current song
        song = self.song_playlist.get(ACTIVE)
        self.song_display.config(text=song, font=('Arial', 11))  # displays the current song above the slider
        song = f'C:/Users/jjdun/Music/Music/{song}'

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
            # mixer.music.unpause()
            # self.pause_state = False
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
        # Make sure the song is considered un-paused and play_state is turned False
        # self.play_time_var = False
        mixer.music.unpause()
        self.pause_state = False

        song = self.song_playlist.get(ACTIVE)  # grabs the currently selected song from the playlist
        song = f'C:/Users/jjdun/Music/Music/{song}'  # adds the file path that was removed in the add_songs function so music.load() can find the song's path
        mixer.music.load(song)  # loads selected song to be played
        mixer.music.play()  # plays the currently loaded song

        if self.play_time_var:
            self.my_slider.config(value=0)
            self.play_time_var = False
            # pass
        else:
            self.play_time()

        # self.play_time_var = True
        # if self.play_time_var:  # if True, reset the slider to 0 to prevent play_time from running 2x


    def stop_music(self):

        # Make sure the song is considered un-paused and play_state is turned False
        mixer.music.unpause()
        self.pause_state = False

        # Reset the slider and status bar
        self.my_slider.config(value=0)
        self.start_time.config(text='')
        self.end_time.config(text='')

        mixer.music.stop()  # stops playing the current song
        self.song_playlist.selection_clear(ACTIVE)  # unselects the current selected song from the playlist

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

        song = self.song_playlist.get(next)
        song = f'C:/Users/jjdun/Music/Music/{song}'  # adding the file path back to the song
        mixer.music.load(song)
        mixer.music.play()

        self.song_playlist.selection_clear(0, END)  # clears the active cursor in the playlist (the 0, END means clear any selected bar from the 1st song to the last song)
        self.song_playlist.activate(next)  # highlights the currently playing song
        self.song_playlist.select_set(next, last=None)  # sets the active bar to the previous song

    def slider(self, x):
        # self.slider_label.config(text=f'{int(self.my_slider.get())} of {int(self.song_length)}')  # temp label, remove when slider is fixed
        # hold_position = int(self.my_slider.get())
        # self.my_slider.config(value=hold_position)

        mixer.music.unpause()
        self.pause_state = False
        # self.play_time_var = True
        song = self.song_playlist.get(ACTIVE)  # gets the currently playing song
        song = f'C:/Users/jjdun/Music/Music/{song}'  # adding the file path back to the song

        mixer.music.load(song)
        mixer.music.play(loops=0, start=int(self.my_slider.get()))  # starts playing the song at the current position of the slider
        self.play_time_var = False
        # self.play_time()

    def volume(self, x):
        mixer.music.set_volume(self.volume_slider.get())  # sets the volume to the current value of the volume slider
        vol = mixer.music.get_volume() * 100  # gets the current volume level
        self.volume_label.config(text=int(vol))

    def shuffle(self):
        # Use self.song_playlist.index(END) to get the last index of the playlist. Create a list from 0 to END then use the random module to output those numbers into another list.
        # To eliminate repeats until all songs are played, try making an if statement or while loop stating: if number in list is played, remove that value at that index and create a list that is one smaller
        # if the size of the list = 0, create another list from 0 to END and randomize it then repeat the process
        pass


MusicPlayer()
from tkinter import *
from PIL import ImageTk, Image
from pygame import mixer
from tkinter import filedialog


class MusicPlayer:

    def __init__(self):

        root = Tk()
        root.geometry('540x400')
        root.resizable(False, False)
        root.title('JD Music Player')

        # Images for the play, stop, pause, rewind, and forward buttons
        back_img = PhotoImage(file='Button_Images/backward.png')
        forward_img = PhotoImage(file='Button_Images/forward.png')
        play_img = PhotoImage(file='Button_Images/play.png')
        pause_img = PhotoImage(file='Button_Images/pause.png')
        stop_img = PhotoImage(file='Button_Images/stop.png')


        # Creating the buttons for the music player
        controls_frame = Frame(root)
        controls_frame.pack(side=BOTTOM, fill='y')


        load_button = Button(controls_frame, text='Load', width=5, font=('Times', 10), command=self.load_music)
        # width controls the size of the button itself, font controls the font of the button and the size of the text
        # try using an image= within the Button function to add the symbols instead of text for each button
        play_button = Button(controls_frame, image=play_img, width=5, font=('Times', 10), command=self.play_music)
        stop_button = Button(controls_frame, image=stop_img, width=5, font=('Times', 10), command=self.stop_music)
        pause_button = Button(controls_frame, image=pause_img, width=5, font=('Times', 10), command=self.pause_music)
        back_button = Button(controls_frame, image=back_img, width=5, font=('Times',10), command=self.rewind_music)
        forward_button = Button(controls_frame, image=forward_img, width=5, font=('Times',10), command=self.next_song)

        # Placing the buttons onto the root window
        load_button.grid(row=0, column=0, columnspan=4)
        play_button.grid(row=0, column=1, columnspan=4)
        # play_button.place(x=110, y=20)
        # pause_button.place(x=220, y=20)
        # rewind_button.place(x=0, y=60)
        # stop_button.place(x=110, y=60)
        # next_button.place(x=220, y=60)

        self.music_file = False  # Initializing this variable for later use. It is given a value of False but will be overwritten later
        self.playing_state = False
        # Might need to add music_file and playing_state as variables in __init__()

        root.mainloop()

    def load_music(self):
        self.music_file = filedialog.askopenfile()  # filedialog.askopenfile() opens a separate window so the user can select the directory to play music from
        # Also consider filedialog.Directory()
        print(self.music_file)

    def play_music(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)  # The file saved in the music_load function will now be loaded
            mixer.music.play()  # Plays the file loaded in music.load()

    def stop_music(self):
        mixer.music.stop()  # Stops the music playback if it is playing. It won't unload the music

    def pause_music(self):
        if not self.playing_state:  # returns True if playing_state = False
            mixer.music.pause()  # Pauses the music if playing_state is False
            self.playing_state = True  # Turns playing_state True after the music is paused
        else:
            mixer.music.unpause()  # Unpauses the music if playing_state is True
            self.playing_state = False  # changes playing_state back to False so it can be paused again

    def rewind_music(self):
        mixer.music.rewind()

    def next_song(self):  # I may have to hard code this function in if pygame does not have a next function
        pass


MusicPlayer()

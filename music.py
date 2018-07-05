import os
import sys
import pygame
import tkinter
import cv2
import mutagen

from pygame import mixer
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import ttk
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

root = Tk()
root.minsize(300,300)

paused = ''
listofsongs = {}
ind = 0
len_of_song = 0

bottomframe = Frame(root)
bottomframe.pack(side= BOTTOM)

leftframe = Frame(root)
leftframe.pack(side = LEFT)

rightframe = Frame(root)
rightframe.pack(side = RIGHT)

topframe = Frame(root)
topframe.pack(side=TOP)

label_title=Label(root)
label_alb=Label(root)
label_art=Label(root)
label_comp=Label(root)
label_genre=Label(root)
label_vol=Label(rightframe)

song_begin = Label(topframe)
song_len = Label(topframe)

def choose_dir():
    """
    Lets the user select the folder
    """
    directory = askdirectory()
    os.chdir(directory)
    index=0
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            listofsongs[index]=file
            index=index+1

choose_dir()
songs = list(listofsongs.values())

select_song =StringVar(root)
select_song.set(songs[0])

def play_music(file):
    global paused
    paused = FALSE
    pygame.init()
    mixer.init()
    mixer.music.load(file)
    mixer.music.play(-1,0.0)

    global ind
    ind = songs.index(file)

    metadata()

def stop_music():
    pygame.quit()

def pause_music():
    global paused
    if not paused:
        pygame.mixer.music.pause()
    if paused:
        pygame.mixer.music.unpause()
    paused = not paused

def play_next():
    global ind
    ind+=1
    if ind >= len(songs):
        ind = 0
    mixer.music.load(listofsongs[ind])
    mixer.music.play(-1,0.0)
    select_song.set(listofsongs[ind])
    metadata()

def play_previous():
    global ind
    ind-=1
    if ind < 0:
        ind = len(songs)-1
    mixer.music.load(listofsongs[ind])
    mixer.music.play(-1, 0.0)
    select_song.set(listofsongs[ind])
    metadata()

def rewind():
    mixer.music.rewind()

def metadata():
    info = EasyID3(listofsongs[ind])
    try:
        title = str(info["title"])[2:-2]
    except:
        title = "------"
    try:
        album = str(info["album"])[2:-2]
    except:
        album = "------"
    try:
        artist = str(info["artist"])[2:-2]
    except:
        artist = "------"
    try:
        composer = str(info["composer"])[2:-2]
    except:
        composer = "------"
    try:
        genre = str(info["genre"])[2:-2]
    except:
        genre = "------"

    global label_title,label_alb,label_art,label_comp,label_genre
    if (label_title.winfo_exists() and label_alb.winfo_exists()
        and label_genre.winfo_exists() and label_art.winfo_exists()
        and label_comp.winfo_exists()
        )==  1:
        label_title.destroy()
        label_comp.destroy()
        label_art.destroy()
        label_genre.destroy()
        label_alb.destroy()

    label_title = Label(topframe,text="SONG TITLE  :  "+title)
    label_title.pack(pady=10)
    label_alb = Label(topframe,text="ALBUM  :  "+album)
    label_alb.pack(pady=10)
    label_art = Label(topframe,text="ARTIST  :  "+artist)
    label_art.pack(pady=10)
    label_comp = Label(topframe,text="COMPOSER  :  "+composer)
    label_comp.pack(pady=10)
    label_genre = Label(topframe,text="GENRE  :  "+genre)
    label_genre.pack(pady=10)

    global song_begin, song_len
    if (song_begin.winfo_exists() and song_len.winfo_exists()) == 1:
        song_begin.destroy()
        song_len.destroy()

    audio = MP3(listofsongs[ind])
    global len_of_song
    len_of_song = audio.info.length

    song_begin = Label(topframe, text="0")
    song_begin.pack(side=LEFT, padx=240)

    song_len = Label(topframe, text=round((len_of_song/(1000*60)%60)*1000,2))
    song_len.pack(side=LEFT, padx=90)

def set_volume(vol):
    mixer.music.set_volume(round(float(vol)/10.0,1))

    vol =int(mixer.music.get_volume()*100)
    check_volume()

def check_volume():
    vol = int(mixer.music.get_volume()*100)
    global label_vol
    if (label_vol.winfo_exists())==1:
        label_vol.destroy()
    label_vol = Label(rightframe,text=vol)
    label_vol.pack(side = TOP,padx=10,pady=40)

def seek_song(value):
    global len_of_song
    val =  float(len_of_song)/float(value)
    if val<round(float(len_of_song),2):
        mixer.music.set_pos(val)
    else:
        mixer.music.rewind()


seek_scale = ttk.Scale(bottomframe,from_= 1,to=5,length=root.winfo_width(),command=seek_song)
seek_scale.pack(side = TOP)

previous_button = Button(bottomframe,text='◄◄(Previous)',command=play_previous)
previous_button.pack(side=LEFT,padx=20,pady=10)

rewind_button = Button(bottomframe,text = "◄◄◄(Rewind)",command=rewind)
rewind_button.pack(side=LEFT,padx=20,pady=10)

stop_button = Button(bottomframe, text="■(Stop)", command=stop_music)
stop_button.pack(side = LEFT,padx=10,pady=10)

pause_button = Button(bottomframe, text="║║(Pause/Resume)", command=pause_music)
pause_button.pack(side=LEFT,padx=10,pady=10)

next_button = Button(bottomframe,text="►►(Next)",command=play_next)
next_button.pack(side=RIGHT,padx=10,pady=10)

menu = OptionMenu(topframe,select_song,*songs,command=play_music)
menu.config(bg="light yellow")
menu.pack()

label_least_vol = Label(rightframe,text="0")
label_least_vol.pack(side=TOP)

label_highest_vol = Label(rightframe,text="100")
label_highest_vol.pack(side=BOTTOM)

volume_scale = ttk.Scale(rightframe,from_= 0,to=10,orient = VERTICAL,command=set_volume)
volume_scale.pack(side = RIGHT,padx=40)

check_Vol = Button(rightframe,text="Volume",command=check_volume,bg="cyan")
check_Vol.pack(side=LEFT)

root.mainloop()
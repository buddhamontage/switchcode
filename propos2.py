from pygame import mixer
import glob
import pygame
#import RPi.GPIO as GPIO
from grove.grove_touch_sensor import GroveTouchSensor
from time import sleep

#when get "GPIO 27 IN" callback this def.
#push btn to change state between pause or not.
def my_callback(channel):
    global btnState
    global pauseState
    global song_index
    if channel==5 and pauseState%2==0:
        btnState = not btnState
        if btnState==touch.on_press:
           mixer.music.unpause()
           pauseState = pauseState+1
    elif channel==5:
        btnState = not btnState
        if btnState==touch.on_press:
            mixer.music.load(songslist[song_index])
            mixer.music.play(0)
        else:
            mixer.music.pause()
            pauseState = pauseState+1
            
#GPIO setup series
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#GPIO.add_event_detect(27,GPIO.RISING,callback=my_callback,bouncetime=200)

#Grove sensor setup series
PIN = 5
touch = GroveTouchSensor(PIN)
touch.on_press = my_callback


btnState=touch.on_release
#get know times of pushing btn
pauseState=1


MUSIC_ENDED = pygame.USEREVENT
pygame.mixer.music.set_endevent(MUSIC_ENDED)
#get all files(songs) from USB
files = glob.glob("/media/usb/*")

#give index number to songs of list
song_index = 0
songslist = [] #all songs in this list

pygame.init()
pygame.mixer.init()

#get each song one by one and detect if it is "MP3" or not.
#push each song in "songslist"
for file in files:
    if file.endswith('.mp3'):
        songslist.append(file)

# always check event to detect end of each song.
# at the end of each song, start next song.
try:
    while True:
        for event in pygame.event.get():
            if event.type == MUSIC_ENDED and songslist[song_index] == songslist[-1]:
                song_index = 0
                pygame.mixer.music.load(songslist[song_index])
                pygame.mixer.music.play()
            
            elif event.type == MUSIC_ENDED:
                song_index += 0
                pygame.mixer.music.load(songslist[song_index])
                pygame.mixer.music.play()
       

except KeyboardInterrupt:
    pass

#GPIO.cleanup()
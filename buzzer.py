import RPi.GPIO as GPIO
import pygame
import glob
from random import *

pygame.init()
pygame.mixer.init()
pygame.mixer.music.stop()

paths=[]
for path in glob.glob("/home/pi/Documents/buzzer/sounds/*.mp3"):
	paths.append(path)


def gpioEvent(channel):
	path = paths[randint(0, len(paths)-1)]
	print(path)
	pygame.mixer.music.load(path)
	pygame.mixer.music.set_volume(1.0)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		continue

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(4, GPIO.FALLING, callback=gpioEvent)

while True:
	continue

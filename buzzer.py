import RPi.GPIO as GPIO #for buzzer event
import pygame           #mp3 player
import glob             #reading file paths
from random import *    #randomly playing the sounds
import threading        #thread for mp3 player


class playerThread(threading.Thread):

	def __init__(self, paths, hitCnt, lock):
		super().__init__()
		self.paths = paths
		self.hitCnt = hitCnt
		self.lastCnt = 0
		self.lock = lock
		pygame.init()
		pygame.mixer.init()
		pygame.mixer.music.stop()

	def run(self):
		while True:
			play = False
			with self.lock:
				if hitCnt > self.lastCnt:
					play = True
			if not play:
				continue

			path = self.paths[randint(0, len(paths) - 1)]
			print(path)
			pygame.mixer.music.load(path)
			pygame.mixer.music.set_volume(1.0)
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy():
				continue
			with self.lock:
				self.lastCnt = hitCnt


paths=[]
for path in glob.glob("/home/pi/Documents/buzzer/sounds/*.mp3"):
	paths.append(path)
hitCnt = 0
lock = threading.Lock()


thread = playerThread(paths, hitCnt, lock)
thread.daemon = True
thread.start()


def gpioEvent(channel):
	global hitCnt
	with lock:
		hitCnt += 1
	print("cnt: " + str(hitCnt))

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(4, GPIO.FALLING, callback=gpioEvent, bouncetime=300)


while True:
	continue

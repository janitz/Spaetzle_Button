import RPi.GPIO as GPIO #for buzzer event 
import pygame #mp3 player 
import glob #reading file paths 
from random import * #randomly playing the sounds 
import threading #thread for mp3 player 
import subprocess
import sys

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
			pygame.mixer.music.set_volume(0.9)
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy():
				continue
			with self.lock:
				self.lastCnt = hitCnt

#audio route headphone jack
subprocess.call('amixer cset numid=3 1', shell=True)
#audio volume
subprocess.call('amixer cset numid=1 90%', shell=True)

paths=[]
for path in glob.glob("sounds/*.mp3"):
	paths.append(path)
hitCnt = 0
lock = threading.Lock()

running = True

thread = playerThread(paths, hitCnt, lock)
thread.daemon = True
thread.start()


def gpioEvent(channel):
	global hitCnt
	global running
	if channel == 4:
		with lock:
			hitCnt += 1
			print("cnt: " + str(hitCnt))
	elif channel == 21:
		running = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(4, GPIO.FALLING, callback=gpioEvent, bouncetime=300)
GPIO.add_event_detect(21, GPIO.RISING, callback=gpioEvent, bouncetime=2000)

print("buzzer ready...")
while running:
	pass
print("buzzer done...")

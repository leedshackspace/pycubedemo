import random
import cubehelper
import os
import math
import pygame

DT = 1.0/10
STARTDELAY = 2.05

def loadsounds(dirname, namelist):
	sounds = []
	for name in namelist:
		newsound = pygame.mixer.Sound(dirname + name + '.wav')
		sounds.append(newsound)
	return sounds

class Pattern(object):

	def init(self):
		pygame.init()
		pygame.mixer.init( )
		pygame.mixer.set_num_channels(1)
		self.isaac = pygame.mixer.Sound('patterns/isaac.wav')
		self.isaacplayed = False
		self.double_buffer = True
		self.timer = 0.0
		return DT

	def tick(self):
		if self.isaacplayed == False and self.timer > STARTDELAY:
			pygame.mixer.stop()
			self.isaac.play()
			self.sleepyplayed = True
		self.timer += DT
		raise StopIteration


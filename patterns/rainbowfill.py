# Rainbow Fill
# Copyright (C) Ian Kernick

import cubehelper
import random
import numpy
import pygame

DT = 1.0/64
MOVE_ANIM_LENGTH = 128 # must be a multiple of 8
FADE_ANIM_LENGTH = 128

# Directions:
# x+ = 0
# x- = 5
# y+ = 1
# y- = 4
# z+ = 2
# z- = 3

class Pattern(object):
	def init(self):
		self.MOVE = 0
		self.FILL = 1
		self.FADE = 2
		
		self.double_buffer = True
		
		
		pygame.init()
		pygame.mixer.init()
		pygame.mixer.set_num_channels(24)
		
		self.fill_sounds = [pygame.mixer.Sound('patterns/rainbowfill-data/fill%d.wav' % f) for f in range(1, 8)]
		self.move_sound = pygame.mixer.Sound('patterns/rainbowfill-data/move.wav')
		
		self.neighbours_coords = []
		self.neighbours_colors = []
		
		self.direction = random.randint(0,5)
		
		self.origin_x = random.randint(0,self.cube.size-1)
		self.origin_y = random.randint(0,self.cube.size-1)
		self.origin_z = random.randint(0,self.cube.size-1)
		
		self.filled = [[[False for x in range(self.cube.size)] for y in range(self.cube.size)] for z in range(self.cube.size)]
		self.pixels = [[[(0.0,0.0,0.0) for x in range(self.cube.size)] for y in range(self.cube.size)] for z in range(self.cube.size)]
		
		self.state = self.MOVE
		self.move_sound.play()
		self.anim_counter = 0
		
		return DT
		
	def validateDirection(self):
		# Make sure the origin position doesn't move out of the cube's boundaries
		if ((self.new_direction == 0 and self.origin_x == self.cube.size -1) or
			(self.new_direction == 5 and self.origin_x == 0) or
			(self.new_direction == 1 and self.origin_y == self.cube.size -1) or
			(self.new_direction == 4 and self.origin_y == 0) or
			(self.new_direction == 2 and self.origin_z == self.cube.size -1) or
			(self.new_direction == 3 and self.origin_z == 0)):
			return False
		else:
			return True
			
	def updateOriginPosition(self):
		# Move the origin position in a direction
		self.cube.set_pixel((self.origin_x, self.origin_y, self.origin_z), (0.0, 0.0, 0.0))
		if (self.direction == 0):
			self.origin_x += 1
		elif (self.direction == 5):
			self.origin_x -= 1
		elif (self.direction == 1):
			self.origin_y += 1
		elif (self.direction == 4):
			self.origin_y -= 1
		elif (self.direction == 2):
			self.origin_z += 1
		elif (self.direction == 3):
			self.origin_z -= 1
		self.cube.set_pixel((self.origin_x, self.origin_y, self.origin_z), (1.0, 1.0, 1.0))
		
	def drawPixel(self, coord, color):
		# Renders the chosen pixel to the cube and then calls findNeighbours()
		self.cube.set_pixel(coord, color)
		self.pixels[coord[0]][coord[1]][coord[2]] = color
		self.findNeighbours(coord, color)
		
	def findNeighbours(self, coord, color):
		# Searches for adjacent pixels that have not been previously added to neighbours_coords
		if color != (0.0,0.0,0.0):
			(x, y, z) = coord
			
			if x != 0 and not self.filled[x-1][y][z]:
				self.addNeighbour((x-1,y,z),color)
			if  x != self.cube.size-1 and not self.filled[x+1][y][z]:
				self.addNeighbour((x+1,y,z),color)
				
			if y != 0 and not self.filled[x][y-1][z]:
				self.addNeighbour((x,y-1,z),color)
			if  y != self.cube.size-1 and not self.filled[x][y+1][z]:
				self.addNeighbour((x,y+1,z),color)
				
			if z != 0 and not self.filled[x][y][z-1]:
				self.addNeighbour((x,y,z-1),color)
			if  z != self.cube.size-1 and not self.filled[x][y][z+1]:
				self.addNeighbour((x,y,z+1),color)
	
	def addNeighbour(self, coord, color):
		# Adds the neighbouring pixel to neighbours_coords and assigns it a colour (but doesn't render it yet)
		self.neighbours_coords.append(coord)
		self.neighbours_colors.append(self.getRandColour(color))
		self.filled[coord[0]][coord[1]][coord[2]] = True
	
	def getRandColour(self, color):
		# Randomly reduces one of the rgb colour channels by a value
		colorList = list(color)
		i = random.randint(0,2)
		colorList[i] -= 0.25
		if colorList[i] < 0:
			colorList[i] = 0.0		
		return (colorList[0], colorList[1], colorList[2])
		
	def tick(self):
		if self.state == self.MOVE:
			if self.anim_counter == 0:
				self.move_sound.play()

			# Move the origin pixel 8 times during the animation
			if self.anim_counter%(MOVE_ANIM_LENGTH/8.0) < 1.0:
				# Change the direction the origin pixel 4 times during the end animation
				if self.anim_counter%(MOVE_ANIM_LENGTH/4.0) < 1.0:
					# The new direction can't be the opposite of the old direction
					self.new_direction = (5 + random.randint(1,5) - self.direction)%6
				
				# If the origin pixel hits an edge, change the direction
				self.direction_valid = self.validateDirection();
				while not self.direction_valid:
					self.new_direction = (5 + random.randint(1,5) - self.direction)%6
					self.direction_valid = self.validateDirection();
				
				# Update the origin pixels position and play sound
				self.direction = self.new_direction
				self.updateOriginPosition()
			
			self.anim_counter += 1
			
			if self.anim_counter == MOVE_ANIM_LENGTH - 1:
				self.state = self.FILL
				sound = random.choice(self.fill_sounds)
				sound.play()
				self.filled = [[[False for x in range(self.cube.size)] for y in range(self.cube.size)] for z in range(self.cube.size)]
				self.filled[self.origin_x][self.origin_y][self.origin_z] = True
				self.anim_counter = 0
		
		elif self.state == self.FILL:
			if self.neighbours_coords == []:
				# First frame
				if self.anim_counter == 0:
					self.drawPixel((self.origin_x, self.origin_y, self.origin_z), (1.0, 1.0, 1.0))
					self.anim_counter += 1
					
				# Last frame
				else:
					self.state = self.FADE
					self.anim_counter = 0
				
			# Middle frames
			else:
				id = random.randint(0, int(len(self.neighbours_coords)*0.8))
				self.drawPixel(self.neighbours_coords[id], self.neighbours_colors[id])
				self.neighbours_coords.pop(id)
				self.neighbours_colors.pop(id)
		
		elif self.state == self.FADE:
			decay = (FADE_ANIM_LENGTH-self.anim_counter-1)/float(FADE_ANIM_LENGTH)
			for x in range(self.cube.size):
				for y in range(self.cube.size):
					for z in range(self.cube.size):
						self.cube.set_pixel((x,y,z), numpy.multiply(self.pixels[x][y][z],decay))
			self.cube.set_pixel((self.origin_x, self.origin_y, self.origin_z), (1.0, 1.0, 1.0))
			
			self.anim_counter += 1
			
			if self.anim_counter == FADE_ANIM_LENGTH - 1:
				self.state = self.MOVE
				self.anim_counter = 0
				raise StopIteration

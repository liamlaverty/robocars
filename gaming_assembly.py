# gaming_assembly.py
# uses pyparticles to create displayed game

import pygame
import pyparticles
import random, math, itertools, time, pickle, datetime
import shutil, os
import argparse
from app_settings import Settings
from new_generation import new_generation
from file_manager import File_Manager

# Train to create save file of best racers, Race to race them on a starting grid
Train = True
Race = False

# declare size of window and track to use
(width, height) = (1200, 450)
track = 'track.bmp'



# given track, place checkpoints
checkpoints = [(400,150),(500,70),(600,60),(640,140),(605,210),(680,300),(720,380),(580,390),(450,350),(320,320),(250,235),(110,325),(60,200),(125,75),(290,90)]

# for ease, define colours here
RED = (255,0,0)
WHITE = (255,255,255)
GREY = (230,230,230)
BLUE = (0,0,255)
BLACK = (0,0,0)

def load_generation_or_new_generation(env, force_new, checkpoints):
	if (force_new == True):
		for i in range(Settings.generation_size):
			fov = random.uniform(0, 90)
			env.addParticles(1, x=checkpoints[0][0], y=checkpoints[0][1], speed=Settings.starting_speed, size=Settings.starting_size)
	else:
		i = 0
		driver_list = File_Manager.load_last_training_file(File_Manager)
		for p in driver_list:	
			fov = random.uniform(0,90)
			env.addParticles(1, x=checkpoints[i][0], y=checkpoints[i][1], speed=Settings.starting_speed, size=Settings.starting_size, control_rods=p.control_rods, bias=p.bias, fov=p.fov)
			i += 1
	return env.particles




def do_training():
	# initiate display and display options
	screen = pygame.display.set_mode((width, height))
	lines = True
	display_checkpoints = True

	# initialise environment
	env = pyparticles.Environment((width, height),image=track,checkpoints=checkpoints,colliding=False)

	
	# add initial particles
	particles_list = load_generation_or_new_generation(env, False, checkpoints=checkpoints)
	# for i in range(Settings.generation_size):	
	# 	fov = random.uniform(0,90)
	# 	env.addParticles(1, x=checkpoints[0][0], y=checkpoints[0][1], speed=Settings.starting_speed, size=Settings.starting_size)

	# display text
	pygame.init()
	pygame.display.set_caption('Generation 1')
	basicfont = pygame.font.Font(None, 32)
	text_string = 'LEADERBOARD'
	header = basicfont.render(text_string, True, RED, WHITE)
	headerRect = header.get_rect()   
	headerRect.center = (800+200, 40)

	n = 0
	while n < Settings.n_generations:

		print('##################')
		generation_caption = '## GENERATION '+str(n+1)+' of '+str(Settings.n_generations)+'##'
		print(generation_caption)
		print('##################')

		pygame.display.set_caption(generation_caption)

		particle_list = env.particles

		# set up background
		track_image = pygame.image.load(track)
		track_rect = track_image.get_rect()
		track_rect.left, track_rect.left = [0,0]

		# initiate run
		pygame.init()
		running = True
		start_time = time.time()
		current_time = time.time()
		

		while current_time - start_time < Settings.duration and running == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			# draw background
			env.update()
			screen.fill(env.colour)
			screen.blit(track_image,track_rect)

			# draw cars and their lines, if requested
			for p in env.particles:
				
				angle = math.pi - p.angle
				fov = p.fov*math.pi/180
				if lines:
					pygame.draw.line(screen, p.colour, (int(p.x), int(p.y)), (int(p.x)+p.distance_front*math.sin(angle),int(p.y)+p.distance_front*math.cos(angle)))
					pygame.draw.line(screen, p.colour, (int(p.x), int(p.y)), (int(p.x)+p.distance_left*math.sin(angle+fov),int(p.y)+p.distance_left*math.cos(angle+fov)))
					pygame.draw.line(screen, p.colour, (int(p.x), int(p.y)), (int(p.x)+p.distance_right*math.sin(angle-fov),int(p.y)+p.distance_right*math.cos(angle-fov)))
				
				pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, p.thickness)

			sorted_list = sorted(particle_list, key=lambda particle:particle.score)[::-1]
			
			### draw leaderboard: particle number, colour, score, controls
			screen.blit(header, headerRect)

			scoreboard_len = min(10,len(sorted_list))
			for i in range(0,scoreboard_len):
				
				p = sorted_list[i]

				leader_x = 800 + 75
				leader_y = 80 + i*35

				numberplate = basicfont.render(str(i+1), True, BLACK, WHITE)
				numberRect = numberplate.get_rect()   
				numberRect.center = (leader_x - 10, leader_y)
				screen.blit(numberplate, numberRect)
				
				pygame.draw.circle(screen, p.colour, (leader_x + 20, leader_y), p.size, p.thickness)
				
				nameplate = basicfont.render(str(p.name), True, BLACK, WHITE)
				nameRect = nameplate.get_rect()   
				nameRect.midleft = (leader_x + 45, leader_y)
				screen.blit(nameplate, nameRect)
				
				scoreplate = basicfont.render(str(round(p.score,3)), True, BLACK, WHITE)
				scoreRect = scoreplate.get_rect()   
				scoreRect.midleft = (leader_x + 100, leader_y)
				screen.blit(scoreplate, scoreRect)		
				
				if p.w:
					wplate = basicfont.render('W', True, BLACK, WHITE)
				else:
					wplate = basicfont.render('W', True, GREY, WHITE)
				wRect = wplate.get_rect()   
				wRect.center = (leader_x + 190, leader_y)
				screen.blit(wplate, wRect)		

				if p.a:
					aplate = basicfont.render('A', True, BLACK, WHITE)
				else:
					aplate = basicfont.render('A', True, GREY, WHITE)
				aRect = aplate.get_rect()   
				aRect.center = (leader_x + 212, leader_y)
				screen.blit(aplate, aRect)		
				
				if p.s:
					splate = basicfont.render('S', True, BLACK, WHITE)
				else:
					splate = basicfont.render('S', True, GREY, WHITE)
				sRect = splate.get_rect()   
				sRect.center = (leader_x + 230, leader_y)
				screen.blit(splate, sRect)		

				if p.d:
					dplate = basicfont.render('D', True, BLACK, WHITE)
				else:
					dplate = basicfont.render('D', True, GREY, WHITE)
				dRect = dplate.get_rect()   
				dRect.center = (leader_x + 250, leader_y)
				screen.blit(dplate, dRect)		

			### draw checkpoints
			if display_checkpoints:
				for pos in checkpoints:
					pygame.draw.circle(screen,RED,pos,5,5)

			pygame.display.flip()
			current_time = time.time()
			env.time_elapsed = int(round((current_time - start_time)*1000))

		### BREED NEW GENERATION ###

		new_generation(particle_list,
		 				pyparticles,
		 				width,
		 				height,
		 				track,
		 				checkpoints)

		File_Manager.save_last_training_file(File_Manager, sorted_list[:Settings.generation_size])

		n += 1

def do_race():

	driver_list = File_Manager.load_last_training_file(File_Manager)

	# initiate race window
	pygame.display.set_caption('Race!')
	screen = pygame.display.set_mode((width, height))
	lines = False
	display_checkpoints = False

	# create starting grid based on initial checkpoint
	spacing = 15
	starting_grid = [(checkpoints[0][0],checkpoints[0][1]),
		(checkpoints[0][0] - spacing, checkpoints[0][1]),
		(checkpoints[0][0], checkpoints[0][1] - spacing),
		(checkpoints[0][0] - spacing, checkpoints[0][1] - spacing),
		(checkpoints[0][0] - 2*spacing, checkpoints[0][1]),
		(checkpoints[0][0], checkpoints[0][1] - 2*spacing),
		(checkpoints[0][0] - 2*spacing, checkpoints[0][1] - spacing),
		(checkpoints[0][0] - 2*spacing, checkpoints[0][1] - 2*spacing),
		(checkpoints[0][0] - spacing, checkpoints[0][1] - 2*spacing),
		(checkpoints[0][0] - 3*spacing, checkpoints[0][1] - spacing)] 

	env = pyparticles.Environment((width, height),image=track,checkpoints=checkpoints,colliding=False)

	# load in drivers
	i = 0
	for p in driver_list:	
		fov = random.uniform(0,90)
		env.addParticles(1, x=starting_grid[i][0], y=starting_grid[i][1], speed=Settings.starting_speed, size=Settings.starting_size, control_rods=p.control_rods, bias=p.bias, fov=p.fov)
		i += 1
	particle_list = env.particles

	# set up background
	track_image = pygame.image.load(track)
	track_rect = track_image.get_rect()
	track_rect.left, track_rect.left = [0,0]

	pygame.init()

	# text preparation
	basicfont = pygame.font.Font(None, 32)
	text_string = 'LEADERBOARD'
	header = basicfont.render(text_string, True, RED, WHITE)
	headerRect = header.get_rect()   
	headerRect.center = (800+200, 40)

	# begin run
	running = True
	start_time = time.time()
	current_time = time.time()
	while current_time - start_time < Settings.duration and running == True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# draw background
		env.update()
		screen.fill(env.colour)
		screen.blit(track_image,track_rect)

		# draw cars
		for p in env.particles:
			angle = math.pi - p.angle
			fov = p.fov*math.pi/180
			if lines:
				pygame.draw.line(screen, p.colour, (int(p.x), int(p.y)), (int(p.x)+p.distance_front*math.sin(angle),int(p.y)+p.distance_front*math.cos(angle)))
				pygame.draw.line(screen, p.colour, (int(p.x), int(p.y)), (int(p.x)+p.distance_left*math.sin(angle+fov),int(p.y)+p.distance_left*math.cos(angle+fov)))
				pygame.draw.line(screen, p.colour, (int(p.x), int(p.y)), (int(p.x)+p.distance_right*math.sin(angle-fov),int(p.y)+p.distance_right*math.cos(angle-fov)))
			pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, p.thickness)

			sorted_list = sorted(particle_list, key=lambda particle:particle.score)[::-1]
			
			### draw leaderboard 

			screen.blit(header, headerRect)

			scoreboard_len = min(10,len(sorted_list))
			for i in range(0,scoreboard_len):
				
				p = sorted_list[i]

				leader_x = 800 + 75
				leader_y = 80 + i*35

				numberplate = basicfont.render(str(i+1), True, BLACK, WHITE)
				numberRect = numberplate.get_rect()   
				numberRect.center = (leader_x - 10, leader_y)
				screen.blit(numberplate, numberRect)
				
				pygame.draw.circle(screen, p.colour, (leader_x + 20, leader_y), p.size, p.thickness)
				
				nameplate = basicfont.render(str(p.name), True, BLACK, WHITE)
				nameRect = nameplate.get_rect()   
				nameRect.midleft = (leader_x + 45, leader_y)
				screen.blit(nameplate, nameRect)
				
				scoreplate = basicfont.render(str(round(p.score,3)), True, BLACK, WHITE)
				scoreRect = scoreplate.get_rect()   
				scoreRect.midleft = (leader_x + 100, leader_y)
				screen.blit(scoreplate, scoreRect)		
				
				if p.w:
					wplate = basicfont.render('W', True, BLACK, WHITE)
				else:
					wplate = basicfont.render('W', True, GREY, WHITE)
				wRect = wplate.get_rect()   
				wRect.center = (leader_x + 190, leader_y)
				screen.blit(wplate, wRect)		

				if p.a:
					aplate = basicfont.render('A', True, BLACK, WHITE)
				else:
					aplate = basicfont.render('A', True, GREY, WHITE)
				aRect = aplate.get_rect()   
				aRect.center = (leader_x + 212, leader_y)
				screen.blit(aplate, aRect)		
				
				if p.s:
					splate = basicfont.render('S', True, BLACK, WHITE)

				else:
					splate = basicfont.render('S', True, GREY, WHITE)
				sRect = splate.get_rect()   
				sRect.center = (leader_x + 230, leader_y)
				screen.blit(splate, sRect)		

				if p.d:
					dplate = basicfont.render('D', True, BLACK, WHITE)
				else:
					dplate = basicfont.render('D', True, GREY, WHITE)
				dRect = dplate.get_rect()   
				dRect.center = (leader_x + 250, leader_y)
				screen.blit(dplate, dRect)		

			# draw checkpoints

			if display_checkpoints:
				for pos in checkpoints:
					pygame.draw.circle(screen,RED,pos,5,5)

		pygame.display.flip()
		current_time = time.time()
		env.time_elapsed = int(round((current_time - start_time)*100000))/100

	# sort the cars, produce a final leaderboard
	sorted_list = sorted(particle_list, key=lambda particle:particle.score)[::-1][:Settings.generation_size]



if Train: do_training()

if Race: do_race()
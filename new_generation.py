# new_generation.py
# either generates a new generation, or gets the most recent one from a file

import pygame
from app_settings import Settings
import itertools, random

def new_generation(particle_list,
                        pyparticles,
                        width,
                        height,
						track,
						checkpoints):
    sorted_list = sorted(particle_list, key=lambda particle:particle.score)[::-1]

    env = pyparticles.Environment((width, height),image=track,checkpoints=checkpoints,colliding=False)
    
    for i in range(Settings.n_to_keep - 1):

        parent_pairs = list(itertools.combinations(range(i+1),2))

        for pair in parent_pairs:
            control_rods,bias,fov,colour = pyparticles.breed(sorted_list[pair[0]],sorted_list[pair[1]])
            env.addParticles(1, x=checkpoints[0][0], y=checkpoints[0][1], speed=Settings.starting_speed, size=Settings.starting_size, control_rods=control_rods, bias=bias, fov=fov, colour=colour)

    while len(env.particles) < (Settings.generation_size - 5):
        parent1 = sorted_list[random.randint(0,Settings.generation_size -1)]
        parent2 = sorted_list[random.randint(0,Settings.generation_size -1)]
        control_rods,bias,fov,colour = pyparticles.breed(parent1,parent2)
        env.addParticles(1, x=checkpoints[0][0], y=checkpoints[0][1], speed=Settings.starting_speed, size=Settings.starting_size, control_rods=control_rods, bias=bias, fov=fov, colour=colour)

    while len(env.particles) < Settings.generation_size :
        env.addParticles(1, x=checkpoints[0][0], y=checkpoints[0][1], speed=Settings.starting_speed, size=Settings.starting_size)

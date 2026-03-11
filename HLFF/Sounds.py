import pyfxr
import random
import time
import pygame

def shot_sound(r=50):
    random.seed(50)#8,18,19 
    pygame.mixer.init()
    # generate sound effect
    #sfx = pyfxr.laser()
    sfx= pyfxr.explosion()
    #sfx =pyfxr.jump()
    sfx=pyfxr.powerup()
    # build waveform
    wave = sfx.build()
    
    # create pygame sound
    sound = pygame.mixer.Sound(buffer=wave)
    
    sound.play()
    #time.sleep(0.1)



def water_splash_sound(r=20):
    random.seed(r) 
    pygame.mixer.init()
    # generate sound effect
    #sfx = pyfxr.laser()
    sfx= pyfxr.explosion()
   
    wave = sfx.build()
    
    # create pygame sound
    sound = pygame.mixer.Sound(buffer=wave)
    
    sound.play()
    #time.sleep(0.1)

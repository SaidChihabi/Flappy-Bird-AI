import pygame
import neat
import time
import os
import random

# Screen constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Make image bigger and load the images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 # For tilting the bird up and down
    ROT_VEL = 20 # How much rotation on each frame
    ANIMATION_TIME = 5 # How long is each animation shown (Flapping speed)

    def __init__(self, x, y):
        self.x = x # Represents the starting
        self.y = y # position of the bird
        self.tilt = 0 # How much image is tilted
        self.tick_count = 0 # Figure out the physics of the bird
        self.vel = 0
        self.height = self.y
        self.img_count = 0 # Which img is shown for the bird so we can animated and keep track
        self.img = self.IMGS[0] # References out bird1.png

    def jump(self): # Bird jump
        self.vel = -10.5 # Number fits and negativ number because top left corner of pygame is 0,0 thats why up is negative vel and down is positiv vel
        self.tick_count = 0 # Keep track to when we last jumped
        self.height = self.y # Keep track where the bird jumped from

    def move(self): # Called every frame to move the bird
        self.tick_count += 1 # Tick happened, frame went by, keep track how many times we move since last jump

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2 # Tickcount how many seconds we been moving

        if d >= 16: # Stop acceleration
            d = 16

        if d < 0:
            d -= 2 # If we moving up lets move a bit more

        self.y = self.y + d # What has been calculated above is been added to the y position

        if d < 0 or self.y < self.height + 50: # if we moving up or as soon as we below the position we jumped from tilt down
            if self.tilt == self.MAX_ROTATION: # So bird doesnt tilt too far
                self.tilt = self.MAX_ROTATION

        else:
            if self.tilt > -90: # Tilt bird down
                self.tilt -= self.ROT_VEL # Rotate the bird 90 degrees

    def draw(self,win): # win is window we drawing on
        self.img_count += 1 # Keep track how many times our loop has run / how many times we shown one img

        # What img to show based on the current img count
        if self.img_count < self.ANIMATION_TIME: # less then 5 (so self.animation_time)
            self.img = self.IMGS[0] #  display first img
        elif self.img_count < self.ANIMATION_TIME * 2: # less then 10
            self.img = self.IMGS[1] # display 2nd img
        elif self.img_count < self.ANIMATION_TIME * 3: # less then 15
            self.img = self.IMGS[2] # display 3rd img
        elif self.img_count < self.ANIMATION_TIME * 4: # less then 20
            self.img = self.IMGS[1] # display 2nd img again
        elif self.img_count == self.ANIMATION_TIME * 4 + 1: # less then 21
            self.img = self.IMGS[0] # display 1st img again
            self.img_count = 0 # restart imgcount to 0

        if self.tilt <= -80: # When bird going down no flapping so we check
            self.img = self.IMGS[1] # Display 2nd img where wings are level
            self.img_cout = self.ANIMATION_TIME * 2 # so it doesnt skip a fram and turns img cout to 10 so it can continue with the if statements from above

        rotated_image = pygame.transform.rotate(self.img, self.tilt) # Rotates an img for us
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center) # From stack overflow
        win.blit(rotated_image, new_rect.topleft) # again stackoverflow (blit means draw)

    def get_mask(self): # For collisions with objects
        return pygame.mask.from_surface(self.img)
    
def draw_window(win, bird): # Draw window of the game
    win.blit(BG_IMG, (0,0)) # Draw Background img on top left position of window
    bird.draw(win) # calls the draw method
    pygame.display.update() # updated the display
    
def main(): # Runs the main loop of the game
    bird = Bird(200,200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # Creates pygame window
    clock = pygame.time.Clock() # Clock obj

    run = True
    while run:
        clock.tick(30) # at most 30 ticks every second
        for event in pygame.event.get(): # keep track when something happend (user input)
            if event.type == pygame.QUIT: # If we click on red x
                run = False # Get out of loop

        #bird.move() # Move the bird every frame
        draw_window(win, bird) # draws bird on the window
    
    pygame.quit() # Pygame quits
    quit() # Quit program

main()





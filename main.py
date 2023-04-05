import pygame
import neat
import time
import os
import random
pygame.font.init()

# Screen constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Make image bigger and load the images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("americantypewriter-bold", 50)

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
    
class Pipe:
    GAP = 200 # How much space inbetween our pipe
    VEL = 5 # How fast pipe is moving (since pipe is moving not bird)

    def __init__(self, x): # only x because the height of tubes is going to be random everytime
        self.x = x
        self.height = 0

        self.top = 0 # Where top of pipe is going to be drawn
        self.bottom = 0 # Where bottom of pipe is going to be drawn
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) # Flipped pipe
        self.PIPE_BOTTOM = PIPE_IMG # and pipe

        self.passed = False # If bird already passed the pipe
        self.set_height() # defines where top and bottom of pipe is and how tall it is (randomly)

    def set_height(self):
        self.height = random.randrange(50, 450) # Where we want top of the pipe to be on screen
        self.top = self.height - self.PIPE_TOP.get_height() # To figure out top of pipe need to figure out top left of pipe img so height and subtract
        self.bottom = self.height + self.GAP

    def move(self): 
        self.x -= self.VEL # move pipe to the left a liltle bit based on what velocity is

    def draw(self,win): # daws pipe
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        # Mask figures out where the pixels in an img are -> so well create two mask (two lists of pixels) and compare them if their coliding with each other (Pixel Perfect Collision), that why we created get_mask earlier
        bird_mask = bird.get_mask() # create the mask for the bird
        top_mask = pygame.mask.from_surface(self.PIPE_TOP) # create mask for top pipe
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM) # and bottom pipe

        # Offset is how far away masks are away from each other
        top_offset = (self.x - bird.x, self.top - round(bird.y)) # Offset of toppipe and bird
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y)) # Offset of bottompipe and bird

        # Figure out if these masks colide
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # Point of collision bottom pipe and bird
        t_point = bird_mask.overlap(top_mask, top_offset) # Point of collision top pipe and bird

        if t_point or b_point: # check if points exist (their not none)
            return True # we are colliding with the other object
        
        return False
    
class Base: # we need class for this because its going to be moving
    VEL = 5 # Same as pipe so it matchess
    WIDTH = BASE_IMG.get_width() # How wide our base img is
    IMG = BASE_IMG

    def __init__(self, y): # starting at a y position( x moving to the left so we dont need to define that)
        self.y = y
        self.x1 = 0 # on screen
        self.x2 = self.WIDTH # directly behin x1

    def move(self): # calling this on every single frame
        self.x1 -= self.VEL # move first img to left
        self.x2 -= self.VEL # move second img to left

        if self.x1 + self.WIDTH < 0: # if image is of the screen
            self.x1 = self.x2 + self.WIDTH # move it to the back

        if self.x2 + self.WIDTH < 0: # same thing here
            self.x2 = self.x1 + self.WIDTH # ...

    def draw(self, win): # the drawing of the base
        win.blit(self.IMG, (self.x1, self.y)) # 1st image
        win.blit(self.IMG, (self.x2, self.y)) # 2nd directly behin based on code above
    
def draw_window(win, bird, pipes, base, score): # Draw window of the game
    win.blit(BG_IMG, (0,0)) # Draw Background img on top left position of window
    for pipe in pipes: # Pipes come at a list and we iterate through them
        pipe.draw(win) # and draw them in the window

    text = STAT_FONT.render("Score " + str(score), 1, (255,255,255)) # text rendering
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10)) #no matter how larger text is always on screen

    base.draw(win) # draw our base
    
    bird.draw(win) # calls the draw method
    pygame.display.update() # updated the display
    
def main(): # Runs the main loop of the game
    bird = Bird(230,250) # bird somewhere in the middle
    base = Base(730) # Height is 800 so 730 height to be at the bottom of the screen
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # Creates pygame window
    clock = pygame.time.Clock() # Clock obj

    score = 0 # keep track of score

    run = True
    while run:
        clock.tick(30) # at most 30 ticks every second
        for event in pygame.event.get(): # keep track when something happend (user input)
            if event.type == pygame.QUIT: # If we click on red x
                run = False # Get out of loop

        #bird.move() # Move the bird every frame
        add_pipe = False
        rem = []
        for pipe in pipes: # creates all the pipes in pipes(list)
            if pipe.collide(bird): # check for collision pipe - bird
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0: # checks if pipe is of the screen
                rem.append(pipe) # puts the pipe in our remove list (so we remove it)

            if not pipe.passed and pipe.x < bird.x: # check if bird passed the pipe
                pipe.passed = True
                add_pipe = True # so as soon bird passes the pipe generate a new one

            pipe.move() # moves the pipe

        if add_pipe: # if we added a pipe
            score += 1 # score increases by one
            pipes.append(Pipe(600)) # and we create a new one (number is to spqn close to each other)

        for r in rem: # iterate through our removed pipes list
            pipes.remove(r) # and remove them

        if bird.y + bird.img.get_height() >= 730:
            pass

        base.move() # moves our base
        draw_window(win, bird, pipes, base, score) # draws bird on the window
    
    pygame.quit() # Pygame quits
    quit() # Quit program

main()





# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [WIDTH/2, HEIGHT/3]
LEFT = False
RIGHT = True
score1 = 0
score2 = 0
score3 = 10
ball_vel = [0, 0]
paddle1_pos = HEIGHT/2-HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_pos = HEIGHT/2-HALF_PAD_HEIGHT
paddle2_vel = 0
paddle2_coord = [PAD_WIDTH, paddle2_pos]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball():  #(direction)
    global score1, score2, score3 
    ball_pos[0] = WIDTH/2 
    ball_pos[1] = HEIGHT/3
    ball_vel[1] =  -random.randrange(4,6) 
    if score2 > score3:
        ball_vel[0] = -random.randrange(3,6)
    elif score2 == score3:
        ball_vel[0] = random.randrange(3,6)
    else:
        ball_vel[0] = random.choice([-6, -5, -4, -3, 3, 4, 5, 6])
        

# define event handlers
def new_game():
    #global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball()
    score1 = 0
    score2 = 0
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, BALL_RADIUS, paddle1_vel, paddle2_vel, score3
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]  
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "red", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    paddle2_coord = [PAD_WIDTH, paddle2_pos]
    paddle2_coord2 =[PAD_WIDTH, paddle2_pos+PAD_HEIGHT]
    
    if paddle1_pos <= 0:
        paddle1_pos = 0
    elif paddle1_pos >= HEIGHT - PAD_HEIGHT:
        paddle1_pos =HEIGHT - PAD_HEIGHT
    if paddle2_pos <= 0:
        paddle2_pos = 0
    elif paddle2_pos >= HEIGHT - PAD_HEIGHT:
        paddle2_pos =HEIGHT - PAD_HEIGHT    

    
        
    # draw paddles
    canvas.draw_line([PAD_WIDTH/2, paddle2_pos],[PAD_WIDTH/2, paddle2_pos+PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH-PAD_WIDTH/2, paddle1_pos],[WIDTH-PAD_WIDTH/2, paddle1_pos+PAD_HEIGHT], PAD_WIDTH, "White")
    
    # determine collisions with borders
    if ball_pos[1] <= 0 + BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[0] == WIDTH/2:
        if ball_vel[0] < 0:
            ball_vel[0] -=1
            print ball_vel[0]
        elif ball_vel[0] > 0:
            ball_vel[0] +=1
            print ball_vel[0]
    
    
    # determine whether paddle and ball collide    
    
    if (ball_pos[1] >= paddle2_pos - BALL_RADIUS):
        if (ball_pos[1] <= paddle2_pos + PAD_HEIGHT + BALL_RADIUS):  #(distance(ball_pos, paddle2_coord) <= BALL_RADIUS or distance(ball_pos, paddle2_coord2) <= BALL_RADIUS)  :
            if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS: 
                ball_vel[0] = -ball_vel[0]
    if (ball_pos[1] >= paddle1_pos - BALL_RADIUS): 
        if(ball_pos[1] <= paddle1_pos + PAD_HEIGHT + BALL_RADIUS):
            if ball_pos[0] >= WIDTH-PAD_WIDTH-BALL_RADIUS:
                ball_vel[0] = -ball_vel[0]		
    if ball_pos[0]<-BALL_RADIUS:
        #ball_vel[0]=ball_vel[1]=0
        score3 = score2
        spawn_ball()
        score2+=1
    elif ball_pos[0]>WIDTH+BALL_RADIUS:
        score1+=1
        #ball_vel[0]=ball_vel[1]=0
        spawn_ball()


    # draw scores
    canvas.draw_text(str(score1), (42, 50), 32, 'white')
    canvas.draw_text(str(score2), (WIDTH-PAD_WIDTH-50, 50), 32, 'white')
    
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle1_vel = 3
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel = -3
    if key == simplegui.KEY_MAP["s"]:
        paddle2_vel = 3
    elif key == simplegui.KEY_MAP["w"]:
        paddle2_vel = -3    
    
    
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle2_vel = 0
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
but_start = frame.add_button('Restart', new_game)

# start frame
#new_game()
frame.start()

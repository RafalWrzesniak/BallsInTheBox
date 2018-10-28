from vpython import *
import numpy as np
import math


# initializing data
scene = canvas(width=550, height=580)
balz_number = 7
user_radius = 1

box_dim = 8
cont = 1
bylo = 0
balls = []
trail = False

# Creating desired amount of balls
for i in range(0, balz_number):
    cont = 1
    if user_radius == 0:
        radius = np.random.uniform(box_dim/40, box_dim/10)
    else:
        radius = user_radius

    balls.append(sphere(radius=radius, color=color.cyan, make_trail=trail, mass=4/3*math.pi*radius**3))
    while cont == 1:
        Check_again = 0
        posx = np.random.uniform(-box_dim / 2 + radius + 0.1, box_dim / 2 - radius - 0.1)
        posy = np.random.uniform(-box_dim / 2 + radius + 0.1, box_dim / 2 - radius - 0.1)
        posz = np.random.uniform(-box_dim / 2 + radius + 0.1, box_dim / 2 - radius - 0.1)
        balls[i].pos = vector(posx, posy, posz)
        for x in range(0, np.size(balls)):
            for y in range(0, np.size(balls)):
                dist = math.sqrt((balls[x].pos.x - balls[y].pos.x) ** 2 + (balls[x].pos.y - balls[y].pos.y) ** 2 + (balls[x].pos.z - balls[y].pos.z) ** 2)
                if dist <= balls[x].radius + balls[y].radius + 0.1 and dist != 0:
                    # print(dist)
                    Check_again = 1
                    cont = 1
                if (x == np.size(balls) - 1 and y == np.size(balls) - 1 and Check_again == 0) or np.size(balls) == 1:
                    cont = 0
    print(len(balls))
    velox = np.random.uniform(-2, 2)
    veloy = np.random.uniform(-2, 2)
    veloz = np.random.uniform(-2, 2)
    balls[i].vel = vector(velox, veloy, veloz)

# Creating box
wallRight = box(pos=vector(box_dim/2, 0, 0), size=vector(0.1, box_dim, box_dim), color=color.red)
wallLeft = box(pos=vector(-box_dim/2, 0, 0), size=vector(0.1, box_dim, box_dim), color=color.blue)
wallTop = box(pos=vector(0, box_dim/2, 0), size=vector(box_dim, 0.1, box_dim), color=color.green)
wallBottom = box(pos=vector(0, -box_dim/2, 0), size=vector(box_dim, 0.1, box_dim), color=color.yellow)
wallBack = box(pos=vector(0, 0, -box_dim/2), size=vector(box_dim, box_dim, 0.1), color=color.white)

t = 0
dt = 0.005

# Simulating balls behavior
while t<100:
    rate(700)
    for ball_nb in range(0,balz_number):
        balls[ball_nb].pos = balls[ball_nb].pos + balls[ball_nb].vel*dt

        if abs(balls[ball_nb].pos.x) >= wallRight.pos.x-balls[ball_nb].radius:
            balls[ball_nb].vel.x = -balls[ball_nb].vel.x
            if balls[ball_nb].pos.x > 0:
                balls[ball_nb].color = wallRight.color
                balls[ball_nb].trail_color = wallRight.color
            else:
                balls[ball_nb].color = wallLeft.color
                balls[ball_nb].trail_color = wallLeft.color

        if abs(balls[ball_nb].pos.y) >= wallTop.pos.y-balls[ball_nb].radius:
            balls[ball_nb].vel.y = -balls[ball_nb].vel.y
            if balls[ball_nb].pos.y > 0:
                balls[ball_nb].color = wallTop.color
                balls[ball_nb].trail_color = wallTop.color
            else:
                balls[ball_nb].color = wallBottom.color
                balls[ball_nb].trail_color = wallBottom.color

        if abs(balls[ball_nb].pos.z) >= abs(wallBack.pos.z)-balls[ball_nb].radius:
            balls[ball_nb].vel.z = -balls[ball_nb].vel.z
            if balls[ball_nb].pos.z < 0:
                balls[ball_nb].color = wallBack.color
                balls[ball_nb].trail_color = wallBack.color
            else:
                balls[ball_nb].color = color.black
                balls[ball_nb].trail_color = color.black

        for ctb in balls:
            dis_bet_balls = math.sqrt((ctb.pos.x - balls[ball_nb].pos.x)**2 + (ctb.pos.y - balls[ball_nb].pos.y)**2 + (ctb.pos.z - balls[ball_nb].pos.z)**2)
            if dis_bet_balls <= ctb.radius + balls[ball_nb].radius and dis_bet_balls != 0:
                old_vel = ctb.vel
                ctb.vel = ctb.vel*((ctb.mass - balls[ball_nb].mass)/(ctb.mass + balls[ball_nb].mass)) + balls[ball_nb].vel * ((2*balls[ball_nb].mass)/(ctb.mass + balls[ball_nb].mass))
                balls[ball_nb].vel = old_vel * ((2*ctb.mass)/(ctb.mass + balls[ball_nb].mass)) + balls[ball_nb].vel * ((balls[ball_nb].mass - ctb.mass)/(balls[ball_nb].mass + ctb.mass))

    t = t + dt

# Droping balls
t = 0
for bal in range(0, balz_number):
    balls[bal].vel = vector(0, -3, 0)

while t < 10:
    rate(1000)
    for bal in range(0, balz_number):
        balls[bal].pos = balls[bal].pos + dt*balls[bal].vel
        if balls[bal].pos.y < wallBottom.pos.y+balls[bal].radius:
            balls[bal].vel = vector(0, 0, 0)
    t = t + dt

import pygame as pg
import random
import time
pg.init()
WIDTH = 1000
HEIGHT = WIDTH
RADIUS = 1

def rand_point():
    x,y = sorted([random.random(), random.random()])
    s,t,u = x,y-x,1-y
    return(s*(WIDTH/2)+ t * (WIDTH-RADIUS) + u*RADIUS,
           s*(RADIUS) + t * (HEIGHT-RADIUS) + u*(HEIGHT-RADIUS))
def main():
    screen = pg.display.set_mode([WIDTH,HEIGHT])
    screen.fill((255,255,255))
    
    pg.draw.circle(screen,(0,0,0), (WIDTH/2,RADIUS),RADIUS)
    pg.draw.circle(screen,(0,0,0), (WIDTH-RADIUS,HEIGHT-RADIUS),RADIUS)
    pg.draw.circle(screen,(0,0,0), (RADIUS,HEIGHT-RADIUS),RADIUS)
    
    last = rand_point()
    pg.draw.circle(screen, (0,0,0), last, RADIUS)
    for x in range (3000):
        #time.sleep(0.005)
        for i in range(100):
            point = random.randrange(3)
            if (point == 0):
                end = ((WIDTH/2), RADIUS)
            elif (point == 1):
                end = (WIDTH-RADIUS, HEIGHT-RADIUS)
            elif(point == 2):
                end = (RADIUS, HEIGHT-RADIUS)
            last = ((last[0]+end[0])/2, (last[1]+end[1])/2)
            pg.draw.circle(screen, (0,0,0), last, RADIUS)
        pg.display.flip()
    print("Done")
main()

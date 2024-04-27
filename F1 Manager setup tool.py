import math;
import random;
import tkinter as tk;
import pyautogui as pg

class Setting:
    over=(0,0)
    stab=(0,0)
    corn=(0,0)
    trac=(0,0)
    stra=(0,0)

def FWA_init():
    FWA = Setting()
    FWA.over = (73/5, -73)
    FWA.stab = (-36/5, 36)
    FWA.corn = (54/5, -54)
    FWA.trac = (-27/5, +27)
    FWA.stra = (-18/5, +18)
    return FWA

def RWA_init():
    RWA = Setting()
    RWA.over = (-146/7, 1825/7)
    RWA.stab = (72/7, -900/7)
    RWA.corn = (90/7, -1125/7)
    RWA.trac = (90/7, -1125/7)
    RWA.stra = (-326/7, 4075/7)
    return RWA

def ARD_init():
    ARD = Setting()
    ARD.over = (9/2, -45/2)
    ARD.stab = (-27/4, 135/4)
    ARD.corn = (27/4, -135/4)
    ARD.trac = (-91/4, 455/4)
    ARD.stra = (0, 0)
    return ARD

def TC_init():
    TC = Setting()
    TC.over = (-45, -139.5)
    TC.stab = (112.5, 348.75)
    TC.corn = (-112.5, -348.75)
    TC.trac = (45, 139.5)
    TC.stra = (0, 0)
    return TC

def TO_init():
    TO = Setting()
    TO.over = (0, 0)
    TO.stab = (72, -36)
    TO.corn = (-18, 9)
    TO.trac = (0, 0)
    TO.stra = (0, 0)
    return TO

class Option():
    score = 0
    setting = [0.0, 0.0, 0.0, 0.0, 0.0]
    handling = [0.0, 0.0, 0.0, 0.0, 0.0]
    
def update_atr(handling, setting, val):
    handling[0] += setting.over[0]*val + setting.over[1]
    handling[1] += setting.stab[0]*val + setting.stab[1]
    handling[2] += setting.corn[0]*val + setting.corn[1]
    handling[3] += setting.trac[0]*val + setting.trac[1]
    handling[4] += setting.stra[0]*val + setting.stra[1]

    return handling

def check_bounds(mins, maxs, handling):
    over = mins[0] <= handling[0] <= maxs[0]
    stab = mins[1] <= handling[1] <= maxs[1]
    corn = mins[2] <= handling[2] <= maxs[2]
    trac = mins[3] <= handling[3] <= maxs[3]
    stra = mins[4] <= handling[4] <= maxs[4]
    return (over and stab and corn and trac and stra)

def find_bounds():
    image = pg.screenshot()
    maxs = []
    mins = []
    row = 434
    edge = 1173

    for _ in range(5):
        row += 53
        min = 1173
        max = 1536
        min_not_found = True
        max_not_found = True
        while(min_not_found):
            px = image.getpixel((min, row))
            if(px[2] > 150 and px[0] < 100):
                min_not_found = False
            else:
                min += 1
        while(max_not_found):
            px = image.getpixel((max, row))
            if(px[2] > 100 and px[0] < 100):
                max_not_found = False
            else:
                max -= 1
        maxs.append(max-edge)
        mins.append(min-edge)

    return (mins, max)

def load_targets(name):
    data = open(name+".txt", "r").readline().split(",")
    handling = [181, 181, 181, 181, 181]
    for i in range(0, len(handling)):
        handling[i] = int(data[i])
    
    return handling

    
def execute(name):

    
    FWA = FWA_init()
    RWA = RWA_init()
    ARD = ARD_init()
    TC = TC_init()
    TO = TO_init()

    mins, maxs = find_bounds()

    targets = load_targets(name):

    best_setting = None

    curOption = Option()
    curOption.handling
    for fa in range (0, 105, 5):
        f = fa/10

        for ra in range(90, 165, 5):
            r = ra/10

            for a in range(9, 0, -1):
                for ca in range(-27, -36, -1):
                    c = ca/10

                    for oa in range (0, 105, 5):
                        handling = [181, 181, 181, 181, 181]
                        o = oa/100

                        handling = update_atr(handling, TO, o)
                        handling = update_atr(handling, TC, c)
                        handling = update_atr(handling, ARD, a)
                        handling = update_atr(handling, RWA, r)
                        handling = update_atr(handling, FWA, f)

                        if (check_bounds(mins, maxs, handling)):
                            valid_setups += 1
                            if(random.randint(1,valid_setups) == 1):
                                best_avg = avg
                                best_set[0] = f
                                best_set[1] = r
                                best_set[2] = a
                                best_set[3] = c
                                best_set[4] = o
                                best_handling = handling

    print("best deviation: ", best_avg)
    print("FWA: ", best_set[0])
    print("RWA: ", best_set[1])
    print("ARD: ", best_set[2])
    print("TC: ", best_set[3])
    print("TO: ", best_set[4])

def main():
    root = tk.Tk()
    root.title("F1 Manager Helper")

    use_file = 0

    tk.Checkbutton(root, text = "Load From file", variable=use_file, onvalue=1, offvalue=0).grid(row = 0, column=0)


    root.mainloop()
    

main()
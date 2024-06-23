import pydirectinput
from pydirectinput import (
    keyDown,
    keyUp,
    move,
    moveRel,
    moveTo,
    mouseDown,
    mouseUp,
    press,
    leftClick,
    rightClick
)
import time

pydirectinput.FAILSAFE=False

def turn(times:int,px:int):
    i=1
    while(i<times):
        move(px,0)
        i=i+1
    i=1

def run(t:int):
    keyDown("w")
    time.sleep(0.01)
    keyDown("shiftleft")
    time.sleep(t/1050)
    keyUp("w")
    keyUp("shiftleft")

def start():
    j=0
    while j!=3:
        time.sleep(0.05)
        press("m")
        j=j+1
    j=0
    time.sleep(1.5)
    leftClick()
    leftClick()
    time.sleep(0.5)
    move(-958,0)
    time.sleep(1)
    turn(20,50)
    time.sleep(0.03)
    leftClick()
    leftClick()
    mouseDown()
    time.sleep(1.2)
    mouseUp()
    time.sleep(0.2)
    moveTo(1498,913)
    time.sleep(0.2)
    leftClick()
    leftClick()
    time.sleep(60)


    i=20
    while(i!=0):
        i=i-1
        moveRel(-320,0,relative=True)
        run(5000)
        #turn(20,-10)
        moveRel(-200,0,relative=True)
        run(3100)
        # turn(20,-30)
        moveRel(-600,0,relative=True)
        run(300)
        time.sleep(0.5)
        keyDown("e")                   #箱1
        time.sleep(1.3)
        keyUp("e")
        #turn(20,54)
        moveRel(1080,0,relative=True)
        run(5710)
        # turn(20,-56)
        moveRel(-1120,0,relative=True)
        run(2300)
        time.sleep(0.5)
        keyDown("e")
        time.sleep(1.3)
        keyUp("e")                      #箱2
        # turn(20,-61)
        moveRel(-1220,0,relative=True)
        run(11500)
        # turn(20,-28)
        moveRel(-550,0,relative=True)
        run(4150)
        # turn(20,-20)
        moveRel(-400,0,relative=True)
        run(100)
        moveRel(0,150,relative=True)
        time.sleep(0.5)
        keyDown("e")                     #桥洞箱
        time.sleep(1.3)
        keyUp("e")
        # turn(20,-90)
        moveRel(0,-150,relative=True)
        moveRel(-1800,0,relative=True)
        run(3500)
        # turn(20,-70)
        moveRel(-1440,0,relative=True)
        run(4700)
        press("2")
        time.sleep(1)
        rightClick()
        time.sleep(1)
        keyDown("s")
        time.sleep(0.55)
        keyUp("s")
        keyDown("a")
        time.sleep(2.8)
        keyUp("a")
        # turn(20,-52)
        moveRel(-1040,0,relative=True)
        run(1400)
        time.sleep(0.5)
        keyDown("e")                        #雕像前一箱
        time.sleep(1.3)
        keyUp("e")
        # turn(20,79)
        moveRel(1580,0,relative=True)
        run(3100)
        # turn(20,20)
        moveRel(420,0,relative=True)
        run(1000)
        time.sleep(0.5)
        keyDown("e")                        #雕像箱子
        time.sleep(1.3)
        keyUp("e")
        # turn(20,-65)
        moveRel(-1300,0,relative=True)
        run(2500)
        # turn(20,-21)
        moveRel(-420,0,relative=True)
        press("1")
        time.sleep(1)
        leftClick()
        time.sleep(1)
        run(6200)
        moveRel(0,150,relative=True)
        time.sleep(0.5)
        keyDown("e")                         #过桥后箱子
        time.sleep(2)
        keyUp("e")
        moveRel(0,-150,relative=True)
        # turn(20,47)
        moveRel(960,0,relative=True)
        run(4300)
        moveRel(0,150,relative=True)
        time.sleep(0.5)
        keyDown("e")                         #瀑布后箱子
        time.sleep(1.3)
        keyUp("e")
        # turn(20,-90)
        moveRel(0,-150,relative=True)
        moveRel(-1800,0,relative=True)
        run(1500)
        # turn(20,44)
        moveRel(880,0,relative=True)
        run(3850)
        moveRel(0,150,relative=True)
        time.sleep(0.5)
        keyDown("e")                         #倒数第二箱
        time.sleep(1.3)
        keyUp("e")
        # turn(20,-20)
        moveRel(0,-150,relative=True)
        moveRel(-400,0,relative=True)
        run(5200)
        # turn(20,50)
        moveRel(1000,0,relative=True)
        run(1550)
        moveRel(0,150,relative=True)
        time.sleep(0.5)
        keyDown("e")                         #最后一箱子
        time.sleep(1.3)
        keyUp("e")
        print("已执行",tabo,"大轮",20-i,"小轮")
        time.sleep(0.5)
        if i>0:
            press("m")
            time.sleep(0.7)
            move(-958,0)
            time.sleep(1)
            turn(20,50)
            time.sleep(0.03)
            mouseDown()
            time.sleep(1.2)
            mouseUp()
            time.sleep(0.2)
            press("m")
            time.sleep(35)

    press("tab")
    keyDown("o")
    time.sleep(4)
    keyUp("o")
    time.sleep(15)

time.sleep(2)

try:
    while True:
        start()
except KeyboardInterrupt:
    ...

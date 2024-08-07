import win32api
import psutil
import pydirectinput
from pathlib import Path
import sys
import logging

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib
import dataclasses
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
    rightClick,
)
import time
from PIL import ImageGrab

pydirectinput.FAILSAFE = False

SETTINGS_PATH = Path(f"./settings.toml")

LOG_FORMAT = r"[%(levelname)s] %(asctime)s : %(message)s"
DATE_FORMAT = r"%Y/%m/%d %H:%M:%S"
logging.basicConfig(
    filename="log.log",
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    encoding="utf-8",
)


@dataclasses.dataclass
class BaseSettings:
    map: str
    interaction: str
    swoop: str
    read: str
    path: str


@dataclasses.dataclass
class TimeSettings:
    waittime: float  # 执行一大轮之后tabo后的等待时间 默认为15
    waittime_after_run: float  # 每次开图时按M后等待时间 默认为0.7
    faliuretime1: float  # 长按着陆点后等待落地时间 默认7
    faliuretime2: float  # 进图后等待时间 默认28
    swordtime: float
    restarttime: float


@dataclasses.dataclass
class RunningSettings:
    mousespeed: int
    circulate: int  # 循环次数 即一大轮要执行多少小轮 默认15
    movetimes: int
    movepx: int  # 控制开图时鼠标移动到最左边后往右移的位移量 (x,y) x移动次数 y代表每次移动像素 默认为(20,50) 有问题请尝试(20,40)
    thelastchest: int  # 最后一箱的跑步距离 默认1580
    landingx: int
    landingy: int
    character: int


@dataclasses.dataclass
class SwitchSettings:
    screen: str  # 分辨率选择
    warlock: bool  # 是否开启术士地狱火版本 开启为true 关闭为false
    sword: bool  # 是否开启故我在挥刀
    Ammo: bool  # 是否开启无绿弹自动切换重弹
    landingerror: bool  # 是否开启检测进图是否成功
    landingerror1: bool
    restart: bool


settings = tomllib.loads(SETTINGS_PATH.read_text("utf-8"))
base_settings = BaseSettings(**settings.pop("base"))
time_settings = TimeSettings(**settings.pop("time"))
run_settings = RunningSettings(**settings.pop("run"))
switch_settings = SwitchSettings(**settings.pop("switch"))

white = (255, 255, 255)
black = (0, 0, 0)
tabo = 0


def turn(times: int, px: int):
    i = 1
    while i < times:
        move(px, 0)
        i = i + 1
    i = 1


def run(t: int):
    keyDown("w")
    time.sleep(0.01)
    keyDown("shiftleft")
    time.sleep(t / 1050)
    keyUp("w")
    keyUp("shiftleft")


def enter1():
    j = 0
    while j != 3:
        time.sleep(1)
        press(base_settings.map)
        j = j + 1
    j = 0
    time.sleep(3)
    leftClick()
    time.sleep(time_settings.waittime_after_run)
    if switch_settings.screen == "1080p":
        move(-958, 0)
    elif switch_settings.screen == "2k":
        move(-1277, 0)
    time.sleep(1)
    turn(20, 50)
    time.sleep(0.1)
    leftClick()
    mouseDown()
    time.sleep(1.2)
    mouseUp()
    time.sleep(0.2)
    moveTo(run_settings.landingx, run_settings.landingy)
    time.sleep(0.2)
    leftClick()


def enter():
    press(base_settings.map)
    time.sleep(time_settings.waittime_after_run)
    if switch_settings.screen == "1080p":
        move(-958, 0)
    elif switch_settings.screen == "2k":
        move(-1277, 0)
    time.sleep(1)
    turn(run_settings.movetimes, run_settings.movepx)
    time.sleep(0.03)
    mouseDown()
    time.sleep(1.2)
    mouseUp()
    time.sleep(0.2)


def color(x, y):
    screenshot = ImageGrab.grab()
    pixel_color = screenshot.getpixel((x, y))
    return pixel_color


def kill_process(process):
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == process:
            proc.kill()


def restart():
    if switch_settings.screen == "1080p":
        if run_settings.character == 1:
            restartx = 1351
            restarty = 466
        elif run_settings.character == 2:
            restartx = 1356
            restarty = 571
        elif run_settings.character == 3:
            restartx = 1362
            restarty = 676
    elif switch_settings.screen == "2k":
        if run_settings.character == 1:
            restartx = 1800
            restarty = 600
        elif run_settings.character == 2:
            restartx = 1800
            restarty = 750
        elif run_settings.character == 3:
            restartx = 1800
            restarty = 900
    kill_process("destiny2.exe")
    time.sleep(60)
    win32api.ShellExecute(
        0,
        "open",
        base_settings.path,
        "",
        "",
        1,
    )
    time.sleep(time_settings.restarttime)
    leftClick()
    leftClick()
    time.sleep(60)
    moveTo(restartx, restarty)
    time.sleep(1)
    leftClick()


def start():
    global tabo
    global white
    global black
    if switch_settings.screen == "1080p":
        x, y = 80, 284
    elif switch_settings.screen == "2k":
        x, y = 106, 375

    enter1()
    if switch_settings.landingerror1:
        reM = 0
        time.sleep(40)
        while True:
            if color(x, y) != white:
                reM = reM + 1
                logging.warning("进图失败！重试次数：%d" % reM)
                press("tab")
                time.sleep(1)
                enter1()
                time.sleep(40)
            else:
                time.sleep(20)
                break
        reM = 0
    else:
        time.sleep(60)

    i = run_settings.circulate
    ammocounter = 0

    while i != 0:
        i = i - 1
        ammocounter = ammocounter + 1
        reM = 0
        reM1 = 0
        if ammocounter == 7 and switch_settings.Ammo:
            logging.info("触发绿弹保底机制！")
            press("F1")
            time.sleep(1)
            if switch_settings.screen == "1080p":
                moveTo(522, 642)
            elif switch_settings.screen == "2k":
                moveTo(700, 850)
            time.sleep(1)
            if switch_settings.screen == "1080p":
                move(-100, 0)
            elif switch_settings.screen == "2k":
                move(-150, 0)
            leftClick()
            time.sleep(1.5)
            leftClick()
            time.sleep(0.5)
            press("F1")
            time.sleep(2)
            ammocounter = 0
        moveRel(round(-320 * 15 / run_settings.mousespeed), 0, relative=True)
        run(5000)
        if switch_settings.warlock:
            press("space")
            time.sleep(0.1)
            press(base_settings.swoop)
            time.sleep(2)
        # turn(20,-10)
        moveRel(round(-200 * 15 / run_settings.mousespeed), 0, relative=True)
        run(3100)
        # turn(20,-30)
        moveRel(round(-600 * 15 / run_settings.mousespeed), 0, relative=True)
        run(300)
        time.sleep(0.5)
        keyDown(base_settings.interaction)  # 箱1
        time.sleep(1.3)
        keyUp(base_settings.interaction)
        # turn(20,54)
        moveRel(round(1080 * 15 / run_settings.mousespeed), 0, relative=True)
        run(5710)
        # turn(20,-56)
        moveRel(round(-1120 * 15 / run_settings.mousespeed), 0, relative=True)
        run(2300)
        time.sleep(0.5)
        keyDown(base_settings.interaction)
        time.sleep(1.3)
        keyUp(base_settings.interaction)  # 箱2
        # turn(20,-61)
        moveRel(round(-1220 * 15 / run_settings.mousespeed), 0, relative=True)
        run(11500)
        # turn(20,-28)
        moveRel(round(-550 * 15 / run_settings.mousespeed), 0, relative=True)
        run(4150)
        # turn(20,-20)
        moveRel(round(-400 * 15 / run_settings.mousespeed), 0, relative=True)
        run(100)
        moveRel(0, round(150 * 15 / run_settings.mousespeed), relative=True)
        time.sleep(0.5)
        keyDown(base_settings.interaction)  # 桥洞箱
        time.sleep(1.3)
        keyUp(base_settings.interaction)
        # turn(20,-90)
        moveRel(0, round(-150 * 15 / run_settings.mousespeed), relative=True)
        moveRel(round(-1800 * 15 / run_settings.mousespeed), 0, relative=True)
        run(3500)
        # turn(20,-70)
        moveRel(round(-1440 * 15 / run_settings.mousespeed), 0, relative=True)
        run(4700)
        if switch_settings.sword:
            press("2")
            time.sleep(1)
            rightClick()
            time.sleep(time_settings.swordtime)
        keyDown("s")
        time.sleep(0.55)
        keyUp("s")
        keyDown("a")
        time.sleep(2.8)
        keyUp("a")
        # turn(20,-52)
        moveRel(round(-1040 * 15 / run_settings.mousespeed), 0, relative=True)
        run(1400)
        time.sleep(0.5)
        keyDown(base_settings.interaction)  # 雕像前一箱
        time.sleep(1.3)
        keyUp(base_settings.interaction)
        # turn(20,79)
        moveRel(round(1580 * 15 / run_settings.mousespeed), 0, relative=True)
        run(3100)
        # turn(20,20)
        moveRel(round(420 * 15 / run_settings.mousespeed), 0, relative=True)
        run(1000)
        time.sleep(0.5)
        keyDown(base_settings.interaction)  # 雕像箱子
        time.sleep(1.3)
        keyUp(base_settings.interaction)
        # turn(20,-65)
        moveRel(round(-1300 * 15 / run_settings.mousespeed), 0, relative=True)
        run(2500)
        # turn(20,-21)
        moveRel(round(-420 * 15 / run_settings.mousespeed), 0, relative=True)
        press("1")
        time.sleep(1)
        leftClick()
        time.sleep(1)
        if switch_settings.warlock:
            press("space")
            time.sleep(0.1)
            press(base_settings.swoop)
            time.sleep(2)
        run(6200)
        moveRel(0, round(150 * 15 / run_settings.mousespeed), relative=True)
        time.sleep(0.5)
        keyDown(base_settings.interaction)  # 过桥后箱子
        time.sleep(2)
        keyUp(base_settings.interaction)
        moveRel(0, round(-150 * 15 / run_settings.mousespeed), relative=True)
        # turn(20,47)
        moveRel(round(960 * 15 / run_settings.mousespeed), 0, relative=True)
        run(4300)
        moveRel(0, round(150 * 15 / run_settings.mousespeed), relative=True)
        time.sleep(0.5)
        keyDown(base_settings.interaction)  # 瀑布后箱子
        time.sleep(1.3)
        keyUp(base_settings.interaction)
        # turn(20,-90)
        moveRel(0, round(-150 * 15 / run_settings.mousespeed), relative=True)
        moveRel(round(-1800 * 15 / run_settings.mousespeed), 0, relative=True)
        run(1500)
        # turn(20,44)
        moveRel(round(880 * 15 / run_settings.mousespeed), 0, relative=True)
        run(3850)
        moveRel(0, round(150 * 15 / run_settings.mousespeed), relative=True)
        time.sleep(0.5)
        keyDown(base_settings.interaction)  # 倒数第二箱
        time.sleep(1.3)
        keyUp(base_settings.interaction)
        # turn(20,-20)
        moveRel(0, round(-150 * 15 / run_settings.mousespeed), relative=True)
        moveRel(round(-400 * 15 / run_settings.mousespeed), 0, relative=True)
        run(5200)
        # turn(20,50)
        moveRel(round(1000 * 15 / run_settings.mousespeed), 0, relative=True)
        run(run_settings.thelastchest)
        moveRel(0, round(150 * 15 / run_settings.mousespeed), relative=True)
        time.sleep(0.5)
        keyDown(base_settings.interaction)  # 最后一箱子
        time.sleep(1.3)
        keyUp(base_settings.interaction)
        time.sleep(0.5)
        press(base_settings.interaction)
        logging.info("已执行%d大轮%d小轮" % (tabo, run_settings.circulate - i))
        time.sleep(0.5)
        if i > 0:
            enter()
            time.sleep(0.1)
            if switch_settings.landingerror:
                while True:
                    if color(x, y) != black:
                        reM = reM + 1
                        logging.warning("进图失败！重试次数：%d" % reM)
                        press(base_settings.map)
                        time.sleep(1)
                        enter()
                        time.sleep(0.1)
                        if switch_settings.restart:
                            if reM > 10:
                                logging.error("检测到游戏崩溃！尝试重启中...")
                                restart()
                                time.sleep(30)
                                enter1()
                                time.sleep(60)
                                enter()
                                reM = 0
                    else:
                        break
                reM = 0
            time.sleep(time_settings.faliuretime1)  # 判断进图成功 等时间着陆
            if switch_settings.landingerror:
                while True:
                    if color(x, y) != white:
                        reM1 = reM1 + 1
                        logging.warning("进图失败！重试次数：%d" % reM)
                        enter()
                        time.sleep(time_settings.faliuretime1)
                        if switch_settings.restart:
                            if reM1 > 10:
                                logging.error("检测到掉线！尝试重启中...")
                                restart()
                                time.sleep(30)
                                enter1()
                                time.sleep(60)
                                enter()
                                reM1 = 0
                    else:
                        break
                reM1 = 0
            time.sleep(time_settings.faliuretime2)

    press("tab")
    keyDown("o")
    time.sleep(4)
    keyUp("o")
    tabo = tabo + 1
    time.sleep(time_settings.waittime)


if switch_settings.screen == "1080p" or switch_settings.screen == "2k":
    print("分辨率设置为" + switch_settings.screen)
else:
    print("分辨率配置错误")
    time.sleep(1000)
if switch_settings.warlock:
    print("术士模式开启中")
else:
    print("术士模式关闭中")
time.sleep(0.2)
if switch_settings.landingerror:
    print("进图检测功能开启中")
else:
    print("进图检测功能关闭中")
time.sleep(0.2)
if switch_settings.sword:
    print("故我在挥刀开启中")
else:
    print("故我在挥刀关闭中")
time.sleep(0.2)
if switch_settings.Ammo:
    print("绿弹保底机制开启中")
else:
    print("绿弹保底机制关闭中")
time.sleep(0.2)
if switch_settings.landingerror1:
    print("轨道进图检测功能开启中")
else:
    print("轨道进图检测功能关闭中")
time.sleep(0.2)
if switch_settings.restart and switch_settings.landingerror:
    print("崩溃检测重进功能开启中")
elif switch_settings.restart and switch_settings.landingerror == 0:
    print("崩溃检测重进功能开启失败！请打开进图检测功能")
    time.sleep(1000)
else:
    print("崩溃检测重进功能关闭中")
time.sleep(0.2)
print(base_settings.read)
logging.info("=======================================")
logging.info("配置文件检测完成")
time.sleep(0.3)
print("5秒后开启程序,请手动切到游戏窗口")
time.sleep(5)
logging.info("程序开始运行")

if __name__ == "__main__":
    try:
        while True:
            start()
    except KeyboardInterrupt:
        ...

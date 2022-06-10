import util
import time
import datetime
import random
import pyautogui


def chaos(common_actions, skills, dungeon_time, timeout):
    start = time.time()
    recalibrate(common_actions)
    while not datetime.time(9, 40) <= datetime.datetime.utcnow().time() <= datetime.time(10, 0): # Stop at daily reset
        dungeon_time_adj = dungeon_time - 5 + util.rand(10)
        try:
            time.sleep(util.rand(1))
            print(f'[{datetime.datetime.now().time()}] Initiate chaos')
            with pyautogui.hold('Alt'):
                pyautogui.keyDown('q')
                time.sleep(0.5 + util.rand(0.2))
                pyautogui.keyUp('q')
                time.sleep(0.1 + util.rand(1))
            x, y = common_actions.match('chaos_dungeon', 0.7, 3)
            time.sleep(util.rand(1))
            util.moveTo(x + 460 + random.randint(5, 15), y + 50 + random.randint(0, 5))
            time.sleep(util.rand(1))
            pyautogui.click()
            x1, y1 = common_actions.match('enter_dungeon', 0.9, 3)
            time.sleep(util.rand(1))
            util.moveTo(x1 + random.randint(5, 15), y1 + random.randint(5, 15))
            time.sleep(util.rand(1))
            pyautogui.click()
            time.sleep(1 + util.rand(1))
            util.press('enter')
            x0, y0 = common_actions.match('leave_dungeon', 0.9, 30)
            util.press('space')
            dungeon_start = time.time()
            time.sleep(5)
            cooldowns = {}
            while time.time() - dungeon_start < dungeon_time_adj:
                pos = common_actions.match('base_resurrect', 0.8)
                if pos is not None:
                    util.moveTo(pos[0] + random.randint(0, 15), pos[1] + random.randint(0, 10))
                    pyautogui.click()
                    time.sleep(5)
                common_actions.match('leave_dungeon', 0.9, 2, verbose=False)
                for key, skill in random.sample(skills.items(), len(skills)):
                    if key in cooldowns and time.time() - cooldowns[key] < skill['cooldown']:
                        continue
                    util.moveTo(random.randint(x0 + (x1-x0)//3, x1), random.randint(y0, y1))
                    pyautogui.rightClick()
                    pyautogui.keyDown(key)
                    cooldowns[key] = time.time() + 0.5
                    time.sleep(skill['duration'] + util.rand(0.1))
                    pyautogui.keyUp(key)
            leave_dungeon(common_actions)
        except TimeoutError:
            print('Chaos failed')
            recalibrate(common_actions)
        if timeout is not None and time.time() - start > timeout:
            break


def recalibrate(common_actions):
    print('Recalibrating')
    common_actions.close_dialogs()
    common_actions.repair()
    leave_dungeon(common_actions)


def leave_dungeon(common_actions):
    pos = common_actions.match('leave_dungeon', 0.9)
    if pos is not None:
        util.moveTo(pos[0] + random.randint(0, 15), pos[1] + random.randint(0, 10))
        pyautogui.click()
        time.sleep(1 + util.rand(1))
        util.press('enter')
        time.sleep(5)
        common_actions.wait_transition()

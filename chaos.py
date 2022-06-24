import util
import time
import datetime
import random
import numpy as np
import pyautogui


def chaos(common_actions, skills, ultimate_mode, dungeon_time, timeout):
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
            dx, dy = common_actions.adjust_position(460, 50)
            util.moveTo(x + dx + random.randint(5, 50), y + dy + random.randint(5, 15))
            time.sleep(util.rand(1))
            pyautogui.click()
            x1, y1 = common_actions.match('enter_dungeon', 0.8, 3)
            time.sleep(util.rand(1))
            util.moveTo(x1 + random.randint(5, 50), y1 + random.randint(5, 20))
            time.sleep(util.rand(1))
            pyautogui.click()
            time.sleep(1 + util.rand(1))
            util.press('enter')
            x0, y0 = common_actions.match('leave_dungeon', 0.8, 30)
            positions = [(x0 + (x1-x0)//3, y0), (x1, y0), (x0 + (x1-x0)//3, y1), (x1, y1)]
            # util.press('tab')
            util.press('space')
            dungeon_start = time.time()
            time.sleep(5)
            abilities = common_actions.abilities()
            if abilities is None:
                print('could not find abilities')
                raise TimeoutError()
            while time.time() - dungeon_start < dungeon_time_adj:
                screenshot = util.get_screen()
                pos = common_actions.match('base_resurrect', 0.8, initial_screenshot=screenshot)
                if pos is not None:
                    util.moveTo(pos[0] + random.randint(0, 15), pos[1] + random.randint(0, 10))
                    pyautogui.click()
                    time.sleep(5)
                common_actions.match('leave_dungeon', 0.8, 2, screenshot, verbose=False)
                if ultimate_mode == 'mayhem':
                    common_actions.press('ability_ultimate')
                current_abilities = common_actions.abilities(screenshot)
                if current_abilities is None:
                    print('could not find abilities')
                    continue
                # player = common_actions.match('player', 0.3, initial_screenshot=screenshot)
                # r, c = util.matches(screenshot, common_actions.templates['enemy'], 0.7)
                # if len(r) > 0:
                #     ay, ax = int(r.mean()), int(c.mean())
                #     if player is not None:
                #         px, py = player
                #         ax += 250 if ax > px - 50 else -250
                #         ay += 250 if ay > py - 50 else -250
                #         print(ax, ay, px, py)
                #     util.moveTo(ax, ay)
                for i, ability in random.sample(list(enumerate(current_abilities)), len(current_abilities)):
                    if np.mean(np.square(abilities[i] - ability)) >= 10:
                        continue
                    pyautogui.rightClick()
                    key = common_actions.keymap[f'ability_{i+1}']
                    util.moveTo(*random.choice(positions))
                    pyautogui.keyDown(key)
                    time.sleep(skills[i] + util.rand(0.1))
                    pyautogui.keyUp(key)
            leave_dungeon(common_actions)
            common_actions.repair()
        except (TimeoutError, pyautogui.FailSafeException):
            print('Chaos failed')
            try:
                recalibrate(common_actions)
            except TimeoutError:
                pass
        if timeout is not None and time.time() - start > timeout:
            break


def recalibrate(common_actions):
    print('Recalibrating')
    common_actions.close_dialogs()
    common_actions.repair()
    leave_dungeon(common_actions)


def leave_dungeon(common_actions):
    pos = common_actions.match('leave_dungeon', 0.8)
    if pos is not None:
        util.moveTo(pos[0] + random.randint(5, 15), pos[1] + random.randint(5, 10))
        pyautogui.click()
        time.sleep(1 + util.rand(1))
        util.press('enter')
        time.sleep(5)
        common_actions.wait_transition()

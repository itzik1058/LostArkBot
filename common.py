import util
import time
import random
import numpy as np
import cv2
import pyautogui


class CommonActions:
    def __init__(self, templates, keymap, game_width, game_height):
        self.keymap = keymap
        self.game_width = game_width
        self.game_height = game_height
        resize = lambda image: cv2.resize(image, dsize=self.adjust_position(*image.shape[:2][::-1]))
        self.templates = {t: resize(image) for t, image in templates.items()}
    
    def adjust_position(self, x, y):
        return x * self.game_height // 900, y * self.game_width // 1600

    def match(self, template, confidence, timeout=None, verbose=True):
        start = time.time()
        result = util.match(self.templates[template], confidence, timeout)
        if verbose and result is not None:
            x, y, c = result
            print(f'{template} with confidence {c:.1%} in {time.time() - start:.1f}s')
            return x, y
        return result
    
    def press(self, key):
        util.press(self.keymap[key])

    def close_dialogs(self):
        print('Attempting to close dialogs')
        for _ in range(5):
            try:
                util.press('Esc')
                self.match('game_menu', 0.8, 1)
                util.press('Esc')
                time.sleep(1)
                break
            except TimeoutError:
                pass

    def repair(self):
        stronghold = self.match('stronghold', 0.8) is not None
        durability = self.match('durability', 0.6) is not None
        if durability and not stronghold:
            print('Entering stronghold')
            self.press('song_stronghold')
            stronghold = True
            time.sleep(10)
            self.wait_transition()
        if stronghold:
            try:
                if durability:
                    print('Initiating durability repair')
                    util.press('g')
                    for button in ('repair_gear', 'tool_repair', 'repair_button'):
                        x, y = self.match(button, 0.7, 5)
                        time.sleep(util.rand(1))
                        util.moveTo(x + random.randint(5, 50), y + random.randint(5, 20))
                        pyautogui.click()
                    self.match('repair_confirm', 0.7, 5)
                    time.sleep(util.rand(1))
                    util.press('Enter')
                    time.sleep(1 + util.rand(1))
                    util.press('Escape')
                    time.sleep(1 + util.rand(1))
            except TimeoutError:
                print('Repair timed out')
                self.close_dialogs()
            print('Exiting stronghold')
            self.press('song_escape')
            time.sleep(10)
            self.wait_transition()
    
    def wait_transition(self):
        try:
            self.match('in_game', 0.8, 30)
        except TimeoutError:
            time.sleep(30)
    
    def abilities(self):
        screenshot = np.array(pyautogui.screenshot(), dtype='uint8')
        match = cv2.matchTemplate(screenshot, self.templates['in_game'], cv2.TM_CCOEFF_NORMED)
        r, c = np.unravel_index(np.argmax(match), match.shape)
        if match[r, c] < 0.8:
            return None
        drt, dct = self.adjust_position(795+20, 795+55), self.adjust_position(525+45, 525+200)
        drb, dcb = self.adjust_position(795+55, 795+95), self.adjust_position(525+65, 525+220)
        abilities = []
        for i in range(4):
            abilities.append(screenshot[r+drt[0]:r+drt[1], c+dct[0]+38*i:c+dct[0]+38*(i+1)])
        for i in range(4):
            abilities.append(screenshot[r+drb[0]:r+drb[1], c+dcb[0]+38*i:c+dcb[0]+38*(i+1)])
        return abilities

import util
import time
import random
import pyautogui


class CommonActions:
    def __init__(self, templates, keymap):
        self.templates = templates
        self.keymap = keymap
    
    def match(self, template, confidence, timeout=None, verbose=True):
        start = time.time()
        result = util.match(self.templates[template], confidence, timeout)
        if verbose and result is not None:
            print(f'{template} found ({time.time() - start:.1f}s)')
        return result
    
    def press(self, key):
        util.press(self.keymap[key])

    def close_dialogs(self):
        print('Attempting to close dialogs')
        for _ in range(5):
            try:
                util.press('Esc')
                self.match('game_menu', 0.9, 1)
                util.press('Esc')
                time.sleep(1)
                break
            except TimeoutError:
                pass

    def repair(self):
        stronghold = self.match('stronghold', 0.9) is not None
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
                        x, y = self.match(button, 0.9, 5)
                        time.sleep(util.rand(1))
                        util.moveTo(x + random.randint(5, 15), y + random.randint(5, 15))
                        pyautogui.click()
                    self.match('repair_confirm', 0.9, 5)
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
            self.match('in_game', 0.9, 30)
        except TimeoutError:
            time.sleep(30)

import util
import time


def fish(common_actions, initial_pos, timeout=None):
    start = time.time()
    recalibrate(common_actions)
    while True:
        try:
            time.sleep(util.rand(1))
            print('Initiate fishing')
            util.moveTo(*initial_pos)
            if len(common_actions.keymap['throw_bait']) == 1:
                common_actions.press('throw_bait')
            common_actions.press('fish')
            common_actions.match('fish', 0.7, 20)
            print('Catch fish')
            time.sleep(util.rand(0.3))
            common_actions.press('fish')
            time.sleep(6)
        except TimeoutError:
            print('Fishing timed out')
            recalibrate(common_actions)
        if timeout is not None and time.time() - start > timeout:
            break


def recalibrate(common_actions):
    print('Recalibrating')
    common_actions.close_dialogs()
    common_actions.repair()
    if common_actions.match('trade_skills', 0.9) is not None:
        util.press('b')
        time.sleep(3)

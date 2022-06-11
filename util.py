import time
import numpy as np
import scipy.interpolate
import cv2
import pyautogui


pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0


def rand(t):
    return np.mean(np.random.exponential(t, 10))


def press(key):
    pyautogui.keyDown(key)
    time.sleep(rand(0.05))
    pyautogui.keyUp(key)


def moveTo(x1, y1):
    for _ in range(5):
        try:
            cp = 4
            x0, y0 = pyautogui.position()
            x, y = np.linspace(x0, x1, cp, dtype='int'), np.linspace(y0, y1, cp, dtype='int')
            r = 50
            xr, yr = np.random.randint(-r, r, cp), np.random.randint(-r, r, cp)
            xr[0] = yr[0] = xr[-1] = yr[-1] = 0
            x, y = x + xr, y + yr
            degree = 3
            tck, u = scipy.interpolate.splprep([x, y], k=degree)
            u = np.linspace(0, 1, 2 + int(np.sqrt(np.square(x0 - x1) + np.square(y0 - y1)) / 30))
            points = scipy.interpolate.splev(u, tck)
            for x, y in zip(*points):
                pyautogui.moveTo(int(x), int(y))
                # time.sleep(0.05 / len(points[0]))
                # time.sleep(np.log2(len(points[0])) / 100)
                time.sleep(0.0001)
            break
        except:
            pass
    # pyautogui.moveTo(x, y, 1, pyautogui.easeInOutQuad)


def match(template, confidence, timeout=None):
    start = time.time()
    while True:
        screenshot = np.array(pyautogui.screenshot(), dtype='uint8')
        match = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        r, c = np.unravel_index(np.argmax(match), match.shape)
        if match[r, c] > confidence:
            return c, r, match[r, c]
        if timeout is None:
            return None
        if time.time() - start > timeout:
            raise TimeoutError()

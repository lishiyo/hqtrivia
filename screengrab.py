# Take a screenshot of quicktime where it is set flush at top left
from PIL import ImageGrab
import os

# full screen width is 2880 x 1800
SCREENSHOT_WIDTH = 850
SCREENSHOT_HEIGHT = 1150

def screenshot(image_path):
    # [x0, y0, x1, y1] - take top left
    img = ImageGrab.grab(bbox=[20, 300, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT])
    img.save(image_path)

if __name__ == '__main__':
    # test path
    test_image_path = os.path.join(os.path.dirname(__file__), 'check.png')
    screenshot(test_image_path)

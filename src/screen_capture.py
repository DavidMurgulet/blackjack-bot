import cv2
import numpy as np
import pyautogui
import pytesseract

class ScreenCapture:
    def __init__(self):
        self.frame_count = 0
        self.prev_val = 0
        self.player_cards = []

    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        return cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    def get_roi(self, img, x1, x2, y1, y2):
        return img[y1:y2, x1:x2]

    def process_roi(self, roi):
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh_roi = cv2.threshold(gray_roi, 127, 255, cv2.THRESH_BINARY)
        return thresh_roi

    def extract_text(self, roi):
        return pytesseract.image_to_string(roi, config="--psm 7").strip()

    def process_frame(self, img):
        screen_height, screen_width, _ = img.shape
        # Define ROIs for player, dealer, and words
        rois = {
            "player": (int(screen_width * 0.44), int(screen_width * 0.48), int(screen_height * 0.78), int(screen_height * 0.85)),
            "dealer": (int(screen_width * 0.48), int(screen_width * 0.53), int(screen_height * 0.51), int(screen_height * 0.56)),
            "words": (int(screen_width * 0.41), int(screen_width * 0.58), int(screen_height * 0.47), int(screen_height * 0.52)),
        }

        # Extract ROIs
        player_roi = self.get_roi(img, *rois["player"])
        dealer_roi = self.get_roi(img, *rois["dealer"])
        words_roi = self.get_roi(img, *rois["words"])

        player_thresh = self.process_roi(player_roi)
        dealer_thresh = self.process_roi(dealer_roi)
        words_thresh = self.process_roi(words_roi)

        # Perform OCR on the thresholded images
        curr_player_value = self.extract_text(player_thresh)
        dealer_value = self.extract_text(dealer_thresh)
        status_msg = self.extract_text(words_thresh)

        return curr_player_value, dealer_value, status_msg
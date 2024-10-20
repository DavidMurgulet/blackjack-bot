import cv2
import numpy as np
import pyautogui
import pytesseract

class ScreenCapture:
    def __init__(self, frame_skip=1):
        self.frame_count = 0
        self.player_cards = []

    def capture_screen(self):
        self.frame_count += 1
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
        config = r'-c tessedit_char_whitelist=0123456789 --psm 7'
        return pytesseract.image_to_string(roi, config=config).strip()

    def process_frame(self, img):
        screen_height, screen_width, _ = img.shape
        # Define ROIs for player, dealer, and words
        rois = {
            # "player": (int(screen_width * 0.445), int(screen_width * 0.48), int(screen_height * 0.78), int(screen_height * 0.85)),
            "player": (int(screen_width * 0.454), int(screen_width * 0.472), int(screen_height * 0.81), int(screen_height * 0.831)),
            # "dealer": (int(screen_width * 0.48), int(screen_width * 0.53), int(screen_height * 0.51), int(screen_height * 0.56)),
            "dealer": (int(screen_width * 0.4915), int(screen_width * 0.509), int(screen_height * 0.519), int(screen_height * 0.542)),
            "words": (int(screen_width * 0.41), int(screen_width * 0.58), int(screen_height * 0.47), int(screen_height * 0.52)),
        }

        # Extract ROIs
        player_roi = self.get_roi(img, *rois["player"])
        dealer_roi = self.get_roi(img, *rois["dealer"])
        words_roi = self.get_roi(img, *rois["words"])

        player_thresh = self.process_roi(player_roi)
        dealer_thresh = self.process_roi(dealer_roi)
        words_thresh = self.process_roi(words_roi)

        # Save the ROIs to the "rois" folder
        cv2.imwrite("rois/player_thresh.png", player_thresh)
        cv2.imwrite("rois/dealer_thresh.png", dealer_thresh)
        cv2.imwrite("rois/words_thresh.png", words_thresh)

        # Perform OCR on the thresholded images
        curr_player_value = self.extract_text(player_thresh)
        dealer_value = self.extract_text(dealer_thresh)
        status_msg = self.extract_text(words_thresh)


        return curr_player_value, dealer_value, status_msg
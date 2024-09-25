import cv2
import pytesseract
import numpy as np
import pyautogui
import time
import keyboard
from strategy import Game

class Bot:
    def __init__(self):
        self.frame_count = 0
        self.game_started = False
        self.player_val = 0
        self.prev_val = 0
        self.player_cards = []

    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        return cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    def create_game(self, player_value, dealer_upcard):
        return Game(player_value, dealer_upcard)

    def end_game(self, game):
        pass

    # called after all cards are
    def check_game_start(self, player_cards, dealer_upcard):
        print(self.player_cards)
        if (len(player_cards) == 2):
            game = self.create_game(player_cards, dealer_upcard)
            self.game_started = True
            return game
        return None
    
            
    def get_roi(self, img, x1, x2, y1, y2):
        return img[y1:y2, x1:x2]

    def process_roi(self, roi):
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh_roi = cv2.threshold(gray_roi, 127, 255, cv2.THRESH_BINARY)
        return thresh_roi

    def extract_text(self, roi):
        return pytesseract.image_to_string(roi, config='--psm 7').strip()


    def get_rois(self, img):
        screen_height, screen_width, _ = img.shape

        # Define ROIs for player, dealer, and words
        rois = {
            'player': (int(screen_width * 0.44), int(screen_width * 0.48), int(screen_height * 0.78), int(screen_height * 0.85)),
            'dealer': (int(screen_width * 0.48), int(screen_width * 0.53), int(screen_height * 0.51), int(screen_height * 0.56)),
            'words': (int(screen_width * 0.41), int(screen_width * 0.58), int(screen_height * 0.47), int(screen_height * 0.52))
        }

        # Extract ROIs
        player_roi = self.get_roi(img, *rois['player'])
        dealer_roi = self.get_roi(img, *rois['dealer'])
        words_roi = self.get_roi(img, *rois['words'])

        return player_roi, dealer_roi, words_roi
        # words_roi = self.get_roi(img, *rois['words'])


                
    def process_frame(self, img):
        """Process the captured frame to extract game data."""
        screen_height, screen_width, _ = img.shape

        # Define ROIs for player, dealer, and words
        rois = {
            'player': (int(screen_width * 0.44), int(screen_width * 0.48), int(screen_height * 0.78), int(screen_height * 0.85)),
            'dealer': (int(screen_width * 0.48), int(screen_width * 0.53), int(screen_height * 0.51), int(screen_height * 0.56)),
            'words': (int(screen_width * 0.41), int(screen_width * 0.58), int(screen_height * 0.47), int(screen_height * 0.52))
        }

        # Extract ROIs
        player_roi = self.get_roi(img, *rois['player'])
        dealer_roi = self.get_roi(img, *rois['dealer'])
        words_roi = self.get_roi(img, *rois['words'])

        # Frame processing, every 3rd frame
        if self.frame_count % 3 == 0:
            player_thresh = self.process_roi(player_roi)
            dealer_thresh = self.process_roi(dealer_roi)
            words_thresh = self.process_roi(words_roi)

            # Perform OCR on the thresholded images
            curr_player_value = self.extract_text(player_thresh)
            dealer_value = self.extract_text(dealer_thresh)
            words_value = self.extract_text(words_thresh)
            
            
            ## if no game 
            if not self.game_started:
                if self.prev_val == 0:
                    self.prev_val = curr_player_value
                    self.player_cards.append(curr_player_value)
                
                # Change in cards
            elif self.prev_val != curr_player_value:
                card_val = int(curr_player_value) - int(self.prev_val)
                self.player_cards.append(card_val)
                self.prev_val = curr_player_value
                
                if len(self.player_cards) == 2:
                    game = self.check_game_start(self.player_cards, dealer_value)
                    if game:
                        result = game.make_decision()
                        if result == "h":
                            pass
                        elif result == "s":
                            pass
            # first loop, prevl val will be 0 curr assigned first card
            
                
                

            # Create game if both player and dealer values are detected'
            # both cards have to be detected and stored by this point 
            game = self.check_game_start(self.player_cards, dealer_value)
            
            # game made if check_game_start returns a game object
            # loop again if game is object, continue looping storing prev and current  bot and 
            # check if player cards change per frame
            
            if game:
                result = game.make_decision()
                # make decision and return right away..
                if result == "h":
                    # Continue to loop until player cards change
                    pass
                elif result == "s":
                    pass
                
            
    def run(self):
        """Main loop to run the bot."""
    
        while True:
            img = self.capture_screen()
            self.process_frame(img)

            # Break on 'q' key press
            if keyboard.is_pressed('q'):
                break

            self.frame_count += 1
            time.sleep(0.05)  # To slow down the capture

        # Release resources
        cv2.destroyAllWindows()

if __name__ == "__main__":
    processor = Bot()
    processor.run()
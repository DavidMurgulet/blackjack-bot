import time
import keyboard
from screen_capture import ScreenCapture
from strategy import Game

class Bot:
    def __init__(self):
        self.frame_count = 0
        self.game_started = False
        self.player_val = 0
        self.prev_val = 0
        self.player_cards = []
        self.screen_capture = ScreenCapture()

    def check_game_start(self, player_cards, dealer_upcard):
        print(self.player_cards)
        if len(player_cards) == 2:
            game = Game(player_cards, dealer_upcard)
            self.game_started = True
            return game
        return None

    def make_decision(self, img):
        # Call the screen_capture processing function
        curr_player_value, dealer_value = self.screen_capture.process_frame(img)


        # TODO: Implement your game logic here

    def run(self):
        while True:
            img = self.screen_capture.capture_screen()
            self.make_decision(img)
  
            if keyboard.is_pressed("q"):
                break

            self.frame_count += 1
            time.sleep(0.05)

if __name__ == "__main__":
    processor = Bot()
    processor.run()
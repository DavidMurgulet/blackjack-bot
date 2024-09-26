import time
import keyboard
from screen_capture import ScreenCapture
from strategy import Game

# every FRAMES frames, we will process the frame
FRAMES = 3

class Bot:
    def __init__(self):
        self.frame_count = 0
        self.game_started = False
        self.player_val = 0
        self.prev_v = 0
        self.player_cards = []
        self.screen_capture = ScreenCapture()

    def start_game(self, player_cards, dealer_upcard):
        if len(player_cards) == 2:
            game = Game(player_cards, dealer_upcard)
            first_decision = game.make_decision()
            self.game_started = True
            print("game started")
            return game, first_decision
        
        print("game not started, some cards missing")
        return None


    def process_game_state(self, img):
        # values per frame
        player_value, dealer_value, status_msg = self.screen_capture.process_frame(img)

        if self.frame_count % FRAMES == 0:
            if not self.game_started:
                # store first player value
                if self.prev_v == 0:
                    self.prev_v = player_value
                    self.player_cards.append(player_value)

                # if player value changes, store the difference
                elif self.prev_v != player_value:
                    card_val = int(player_value) - int(self.prev_v)
                    self.player_cards.append(card_val)
                    self.prev_v = player_value

                    # Check if the dealer has a value and the player has 2 cards
                if dealer_value != "" and len(self.player_cards) == 2:
                    game = self.start_game(self.player_cards, dealer_value)
                    action = game.make_decision()



                    #TODO: implement yolo training to detect card
                    # action returns inital decision
                        # give to yolo to detect button + pythongui to hit button
                        # if action == "h":
                            # 



            # game started check for player cards added
            else:
                pass


    def run(self):
        while True:
            img = self.screen_capture.capture_screen()
            self.process_game_state(img)
  
            if keyboard.is_pressed("q"):
                break

            self.frame_count += 1
            time.sleep(0.05)

if __name__ == "__main__":
    processor = Bot()
    processor.run()
import time
import keyboard
from screen_capture import ScreenCapture
from strategy import Game
import sys
import select
# import yolo_detections

#TODO: implement yolo training to detect card
        # action returns inital decision
        # give to yolo to detect button + pythongui to hit button


# plan


#  bot is the main running will run the Game
#       it uses the ScreenCapture class 
#           to get video every frame, get rois and get what they read with ocr (pytesseract)
#           then return to the bot, along with the original frame

#       bot will send frame to yolo class, where frame will be processed and run on yolo (detect)
#           yolo will detect the betting area, the betting options, and the hit stand double split buttons and send to bot
#           bot will then send the decision to the pythongui class to click the button

#           if yolo detects both betting option + bet button, send to bot,
#           else if it detects both hit and stand and other options, send to bot
#           if nothing is detected, do nothing?

 
#           if both betting options are detected, check bet_placed = True (bot class) + bet_amount = True (bot class)


#           check given to bot bet_placed = True + amount = True
#           
# 
#  
#
#               decision is made by the bot based off of what is detected etc.
#                  bot will then send the decision to the pythongui class to click the button 
#                   bot will have vars =  
#                       bet_placed = False
#                       bet_amount = 0
#                       decision = None
#                       game_started = False
#                       player_val = 0
#                       prev_v = 0
#                       player_cards = []
#                       screen_cap = ScreenCapture()
#                       m_game = None



# every FRAMES frames, we will process the frame
FRAMES = 3
USR_BET_AMOUNT = 0

class Bot:
    def __init__(self):
        self.frame_count = 0
        self.game_started = False
        self.player_val = 0
        self.prev_v = None
        self.prev_dv = 0
        self.player_cards = []
        self.screen_cap = ScreenCapture()
        self.m_game = None
        self.bet_amount = 0
        self.bet_placed = False
        self.decision = None
        self.player_ace = False

    def start_game(self, player_cards, dealer_upcard):
        if len(player_cards) == 2 and dealer_upcard != "":
            game = Game(player_cards, dealer_upcard)
            first_decision = game.make_decision()
            self.game_started = True
            print("game started")
            return game, first_decision
        
        print("game not started, some cards missing")
        return None

    def is_there_game(self):
        pass

    def end_game(self):
        pass

    def process_game_frame(self, img):
        player_value, dealer_value, status_msg = self.screen_cap.process_frame(img)
        print(f"Player Value: {player_value}, Dealer Value: {dealer_value}, Status: {status_msg}")
        if (player_value == 1 or player_value == 11):
            self.player_ace = True

        # self.bet_amount, self.bet_placed, hit, split, double, stand = yolo_detection.detect(img)

        # if bet has not been placed yet
            # check if betting is avaialble
            # if betting is available, place bet
            # set bet_placed = True

        # if decisions are detectable, make decision (stored in bot)
            # use pythonjui to click button
            # if decision is stand or double, the no more decisions will be made, only count dealer cards.
            # if decision is split, then split the game into 2 games
            # if decision is hit, then add card to game

        # if bet has been placed, now wait for game to start
        # check if currently in game
        if not self.game_started:
                # store first player value
               # Initialize previous value to None to differentiate first input from subsequent inputs
            if self.prev_v is None and player_value != "":
            # First card detection
                self.prev_v = player_value
                print("First player value detected:", player_value)
                self.player_cards.append(player_value)

# If the player value changes and is not ","
        elif player_value != "":
        # Check if previous value is valid and player value is valid
            if self.prev_v is not None and self.prev_v.isdigit() and player_value.isdigit():
        # Calculate the card value difference
                card_val = int(player_value) - int(self.prev_v)
                self.player_cards.append(card_val)
                print("New card added:", card_val)
                self.prev_v = player_value

        # Check if the dealer has a value and the player has 2 cards
                game, first_decision = self.start_game(self.player_cards, dealer_value)
                if game is not None:
                    self.m_game = game
                    self.decision = first_decision
                    return
            else:
            # Update prev_v to current player value if it's valid
                self.prev_v = player_value
               

                    
                    #hit case
        elif self.game_started:
            if self.decision == "hit":
                # continously loop until player val changes, then do the math and add it to game and make decision
                self.check_new_card(player_value)
            if self.decision == "stand":
                self.check_dealer_card(dealer_value)
                pass


            if self.decision == "d":
                #
                self.end_game()


            if self.decision == "sp":
                pass
        
    
    def check_dealer_card(self, dealer_value):
        if self.prev_dv != dealer_value:
            card_val = int(dealer_value) - int(self.prev_dv)
            self.m_game.dealer_hand.append(card_val)
            self.prev_dv = dealer_value

            # Check if dealer has stopped drawing cards
            if self.m_game.dealer_stands():
                self.end_game()
        pass


    def check_new_card(self, player_value):
        if (self.prev_v != player_value):
            card_val = int(player_value) - int(self.prev_v)
            self.player_cards.append(card_val)
            ## update new decision 
            self.decision = self.m_game.new_card(card_val)
            self.prev_v = player_value 


    def end_game(self):
        self.game_started = False
        self.player_val = 0
        self.prev_v = 0
        self.player_cards = []
        self.m_game = None
        self.bet_amount = 0
        self.bet_placed = False
        self.decision = None

    def run(self):
        while True:
            img = self.screen_cap.capture_screen()
            self.process_game_frame(img)
  
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                input_line = sys.stdin.readline().strip()
                if input_line.lower() == "stop":
                    break
         

            self.frame_count += 1
            time.sleep(0.05)

if __name__ == "__main__":
    processor = Bot()
    processor.run()
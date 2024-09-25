#rules, chosen by player.
double_down_ace= False
split_on = False


player_hand = [] # list of cards
dealer_upcard = 0
bet_amount = 0
auto_bet = False

# YOLO training: 
#   hit stand double split
#   bet button
#   bet options
#   quit


# have player value and dealer upcard
    # TODO: have player values seperate
    
# main py == capture screen + preprocessing 
#     -> yolo detection === gives me hit stand etc PER frame
#     -> main.py give player value and dealer upcard PER frame
#             -> strategy.py does math and gives me hit stand logic etc PER frame
#                 -> main.py takes that logic and clicks with pythongui per frame


# NEEDS DETECTION FOR GAME END (blackjack, bust, win, lose)
class Game:
    def __init__(self, first_card, dealer_upcard):
        self.player_hand = [{first_card}]
        self.dealer_upcard = dealer_upcard
        self.double_possible = False
        self.split_possible = False

    def new_card(self, card):
        self.player_hand.append(card)

    def hit_or_stand(self):
        player_total = sum(self.player_hand)
        has_ace = 1 in self.player_hand

        # Adjust the dealer upcard for Ace case (treat dealer ace as 11)
        dealer_upcard = self.dealer_upcard
        if dealer_upcard == 1:
            dealer_upcard = 11

        # Check if it's a soft hand (has ace counted as 11)
        if has_ace and player_total <= 11:
            # Soft totals logic
            if player_total == 11:  # A,9
                if dealer_upcard in [2, 3, 4, 5, 6]:  # Dealer upcard 2-6
                    return "S"
                else:
                    return "S"
            elif player_total == 10:  # A,8
                return "S"
            elif player_total == 9:  # A,7
                if dealer_upcard in [3, 4, 5, 6]:  # Dealer upcard 3-6
                    return "Ds"
                elif dealer_upcard in [2, 7, 8]:
                    return "S"
                else:
                    return "H"
            elif player_total == 8:  # A,6
                if dealer_upcard in [3, 4, 5, 6]:
                    return "Dh"
                else:
                    return "H"
            elif player_total == 7:  # A,5
                if dealer_upcard in [4, 5, 6]:
                    return "Dh"
                else:
                    return "H"
            elif player_total == 6:  # A,4
                if dealer_upcard in [4, 5, 6]:
                    return "Dh"
                else:
                    return "H"
            elif player_total == 5:  # A,3
                if dealer_upcard in [5, 6]:
                    return "Dh"
                else:
                    return "H"
            elif player_total == 4:  # A,2
                if dealer_upcard in [5, 6]:
                    return "Dh"
                else:
                    return "H"
        
        # Hard totals logic
        else:
            if player_total >= 17:  # 17 or higher
                return "S"
            elif player_total == 16:
                if dealer_upcard in [2, 3, 4, 5, 6]:
                    return "S"
                else:
                    return "H"
            elif player_total == 15:
                if dealer_upcard in [2, 3, 4, 5, 6]:
                    return "S"
                else:
                    return "H"
            elif player_total == 14:
                if dealer_upcard in [2, 3, 4, 5, 6]:
                    return "S"
                else:
                    return "H"
            elif player_total == 13:
                if dealer_upcard in [2, 3, 4, 5, 6]:
                    return "S"
                else:
                    return "H"
            elif player_total == 12:
                if dealer_upcard in [4, 5, 6]:
                    return "S"
                else:
                    return "H"
            elif player_total == 11:
                return "Dh"
            elif player_total == 10:
                if dealer_upcard in [2, 3, 4, 5, 6, 7, 8, 9]:
                    return "Dh"
                else:
                    return "H"
            elif player_total == 9:
                if dealer_upcard in [3, 4, 5, 6]:
                    return "Dh"
                else:
                    return "H"
            else:  # 8 or less
                return "H"
            
            
        def split_decision(self):
            pass
        
        def double_decision(self):
            pass
        
        def hit_decision(self):
            pass
        
        def stand_decision(self):
            pass
        

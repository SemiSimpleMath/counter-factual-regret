import cnfg
import dict_utilities
import hand_strength
import hand_functions

def generate_deck():

    deck = []

    for i in range (0,13):
        for j in range (0,4):
            deck.append((i,j))
    return deck

def init():
    cnfg.MCT = dict_utilities.load_mct_dict() # MCT is the Monte Carlo hand vs hand strength dictionary
    cnfg.HS = hand_functions.generate_two_card_hands() # HS is all possible two card hands
    cnfg.FS = hand_functions.generate_hand_pairs() # FS is set of all possible hand vs hand (2 cards vs 2 cards)
    cnfg.SF_LIST = hand_functions.generate_sf_list(cnfg.HS) # SF_LIST is a list of cards in standard form.  This is very compact list of possible one player hands it only contains info about hand rank and if it is suited or not
    hand_strength.generate_sf_hand_vs_sf_hand_table()
    cnfg.DECK = generate_deck()
 


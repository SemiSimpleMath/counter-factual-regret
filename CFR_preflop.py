
import random
import init
import cnfg
import hand_functions
import hand_strength

class Node:
    def __init__(self, action_list, card):
        self.action_list = action_list
        self.card = card
        self.times_visited = 0
        self.possible_actions=self.get_possible_actions(action_list)
        self.regrets = dict() # init to 0s
        self.cumulative_regrets = dict() # init to 0s
        self.average_regrests = dict() #inits to 0s
        self.average_strategy = dict()
        self.strategy = dict() #init to equal prob for each possible action
        self.strategy_sum = dict()
        self.utility = dict()
        self.is_terminal = False
        self.init_data_lists()
        return

    def init_data_lists(self):

        if self.is_terminal:
            return
        num_actions = len(self.possible_actions)
        for item in self.possible_actions:
            self.utility[item] = 0
            self.regrets[item] = 0
            self.cumulative_regrets[item] = 0
            self.strategy[item] = (1/num_actions)
            self.strategy_sum[item] = (1/num_actions)
            self.average_strategy[item] = 0
        return

    def get_possible_actions(self, action_list=None):

        possible_actions = []

        if action_list == None:
            action_list = self.possible_actions

        if len(action_list) == 0:
            possible_actions = [1,2,3]

        if len(action_list) == 1:
            if action_list[-1] == 3:
                possible_actions = [0,1]
            elif action_list[-1] == 2:
                possible_actions = [0,1,2,3]
            elif action_list[-1] == 1:
                possible_actions = [1,2,3]

        if len(action_list) > 1:
            if action_list[-1] == 3:
                possible_actions = [0,1]
   
            elif action_list[-1] == 2:
                possible_actions = [0,1,2,3]
            
        if len(action_list) >= 3:
            if action_list[-3:] == [2,2,2]:
                possible_actions = [0,1,3]   

        return possible_actions

    def is_terminal_node(self, action_list):
        self.is_terminal = False

        if len(action_list) == 0:
            return False
        
        if len(action_list) == 1 and action_list[0] == 1:
            return False

        if action_list[-1] == 0 or action_list[-1] == 1:
            self.is_terminal = True
            return True

        return False
        


    def compute_regret(self, total_utility):
        for key in self.utility.keys():
            self.regrets[key] = self.utility[key] - total_utility

    def update_cumulative_regret(self, reach_probability):
        for key in self.cumulative_regrets.keys():
            self.cumulative_regrets[key] += reach_probability * self.regrets[key]

    def update_strategy(self, realization_weight=1):
        strat_sum = 0
        for key in self.strategy.keys():
            self.strategy[key] = self.cumulative_regrets[key] if self.cumulative_regrets[key] > 0 else 0
            strat_sum += self.strategy[key]

        for key in self.strategy.keys():
            if strat_sum > 0:
               self.strategy[key] = self.strategy[key] / strat_sum
            else:
                self.strategy[key] = 1 / len(self.strategy)
            self.strategy_sum[key] += realization_weight * self.strategy[key]
        return

    def compute_average_strategy(self):

        normalizing_sum = sum(self.strategy_sum.values())
        for key in self.strategy_sum.keys():
            if normalizing_sum > 0:
                self.average_strategy[key] = self.strategy_sum[key] / normalizing_sum
            else:
                self.average_strategy[key] = 1 / len(self.strategy_sum)
        return self.average_strategy




def pick_action_list():

    action_lits = [[], [0], [1], [0,1]] # these are non-terminal action_lists

    return action_lists[random.randomint(0, len(action_lists) )]



def get_terminal_utility(action_list, cards):

    if action_list[-1] == 1:
        ev = get_ev_of_call(cards,action_list)
    else:
        ev = get_ev_of_fold(action_list)

    return ev

def CFR_minimization(node, action_list, cards, reach_probability_1, reach_probability_2):

    player = len(action_list) % 2

    if node.is_terminal_node(action_list):
        return get_terminal_utility(action_list, cards)


    possible_actions = node.get_possible_actions(action_list) #this needs to be done

    total_utility = 0
    for action in possible_actions:

        action_prob = node.strategy[action]

        child_node = get_node(action_list + [action], cards)

        if player == 0:
            node.utility[action] = - CFR_minimization(child_node, action_list + [action], cards, action_prob * reach_probability_1 , reach_probability_2) 
        elif player == 1:
            node.utility[action] = - CFR_minimization(child_node, action_list + [action], cards,  reach_probability_1, action_prob * reach_probability_2) 

        total_utility += action_prob * node.utility[action]


    node.compute_regret(total_utility)
    if player == 0:
        reach_probability = reach_probability_2
    else:
        reach_probability = reach_probability_1

    node.update_cumulative_regret(reach_probability)
    node.update_strategy(reach_probability) # really reach here?
    return total_utility    



      

def get_node(action_list, cards):
    player = len(action_list) % 2

    card = cards[player]

    action_tuple = tuple(action_list)

    dict_key = (action_tuple, card)

    if dict_key in node_dict:
        node = node_dict[dict_key]
    else:
        node = Node(action_list,card)
        node_dict[dict_key] = node

    return node





drawn_cards = dict()

def draw_cards():
    cards = random.sample(cnfg.DECK, 4)
    card1,card2,card3,card4 = cards

    hand1 = (card1,card2)
    hand1 = hand_functions.order_hand(hand1)

    hand2 = (card3,card4)
    hand2 = hand_functions.order_hand(hand2)

   # hand1,hand2 = hand_functions.prepare_pair(hand1, hand2)
    hand1 = hand_functions.adjust_pair_order(hand1)
    hand2 = hand_functions.adjust_pair_order(hand2)

    drawn_cards[hand1] = "T"

    return hand1,hand2

def train(num_steps):
    for i in range(0, num_steps):
        cards = draw_cards()

        action_list = []
        node = get_node(action_list, cards)
        CFR_minimization(node,action_list, cards, 1, 1)

        if i % 10000 == 0:
            print (i)
    

def get_ev_of_call(cards, action_list): 
    

    hand1 = cards[0]
    hand2 = cards[1]

    hand1, hand2 = hand_functions.prepare_pair(hand1,hand2)
    win_data = cnfg.MCT[(hand1, hand2)]
 
    player = (len(action_list) + 1) % 2 # player who took last action

    wrt, ties, junk = win_data
    
    lrt = 1 - wrt - ties

    if player == 1:
        wrt_temp = lrt
        lrt = wrt
        wrt = wrt_temp

    pots, amounts, money_put_in  = hand_functions.calculate_pot_from_action_list(action_list)
    
    pot_at_end = pots[-1]
    
    pot_to_win = pot_at_end - money_put_in[player]
    
    
    ev = wrt * pot_to_win - lrt * money_put_in[player]
    
    return -ev
    



def get_ev_of_fold(action_list):
    pots, amounts, money_put_in  = hand_functions.calculate_pot_from_action_list(action_list)
    #get money put in by folding player
    player = (len(action_list)+1) % 2 # check this
    ev = money_put_in[player]
    return ev




    
def look_up_hand_vs_hand(hand1, hand2):
    # hand1 and hand2 assumed to have been prepared to be compatible 
    key = (hand1,hand2)
    return hand_table[key] # global hand_table




def compute_average_strategy(node_dict):
    for node in node_dict.values():
        if not node.is_terminal:
            node.compute_average_strategy()
    return


def print_results(node_dict):

    for node in node_dict.values():
        if not node.is_terminal:
            print ("Action lists:", node.action_list)
            print ("Card: ", node.card)
          #  print (node.strategy)
            print (node.average_strategy)
            print ("\n")

    return



def save_data_dict(path, data_dict):
    import pickle
    pickle.dump( data_dict, open( path + "CFR_optimal_dict_3.p", "wb" ) )


def create_data_dict(node_dict):
    data_dict = dict()

    for node in node_dict.values():
        if not node.is_terminal:
            action_list = node.action_list
            action_tuple = tuple(action_list)
            card = node.card
            key = (action_tuple,card)
            data_dict[key] = node.average_strategy

    return data_dict

def load_optimal_dict(path, file):
    import pickle
    infile = open(path + file,'rb')
    optimal_dict = pickle.load(infile)
    infile.close()

    return optimal_dict

node_dict = dict()

init.init()

train(5000000) # million takes about 10 min to run.  few ten million is reasonable to run
compute_average_strategy(node_dict)
#print_results(node_dict)


# save the range dict
data_dict = create_data_dict(node_dict)
save_data_dict("data/dicts/", data_dict)
optimal_dict = load_optimal_dict("data/dicts/", "CFR_optimal_dict_3.p" )

print ("OPTIMAL DICT")
print (len(optimal_dict))
print (len(drawn_cards))
print (len(node_dict))
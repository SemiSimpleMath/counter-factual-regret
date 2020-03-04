
import random

node_dict = dict()

class Node:
    def __init__(self, action_list, card):
        self.action_list = action_list
        self.card = card
        self.times_visited = 0
        self.possible_actions=[0,1]
        self.regrets = [0,0]
        self.cumulative_regrets = [0,0]
        self.average_regrests = [0,0]
        self.strategy = [.5,.5]
        self.strategy_sum = [.5,.5]
        self.is_terminal_node = False
        return



def draw_cards():
    cards = [0,1,2]
    p_cards = random.sample(cards,2)

    return p_cards

def pick_action_list():

    action_lits = [[], [0], [1], [0,1]] # these are non-terminal action_lists

    return action_lists[random.randomint(0, len(action_lists) )]


def is_terminal_node(action_list):

    if action_list == [0,0] or action_list == [0,1,0] or action_list == [0,1,1] or action_list == [1,1]   or action_list == [1,0]:
        return True
    else:
        return False


def get_terminal_utility(action_list, cards):

    if action_list == [1,1]:
        if cards[0] > cards[1]:
            return 2
        else:
            return -2

    if action_list == [0,1,1]:
        if cards[0] > cards[1]:
            return -2
        else:
            return 2

    if action_list == [0,0]:
        if cards[0] > cards[1]:
            return 1
        else:
            return -1

    if action_list == [0,1,0]:
        return 1

    if action_list == [1,0]:
        return 1


def CFR_minimization(node, action_list, cards, reach_probability_1, reach_probability_2):

    player = len(action_list) % 2

    if is_terminal_node(action_list):
        return get_terminal_utility(action_list, cards)

    utility = [0,0]
    total_utility = 0

    possible_actions = [0,1]

    for action in possible_actions:

        action_prob = node.strategy[action]

        child_node = get_node(action_list + [action], cards)

        if player == 0:
            utility[action] = - CFR_minimization(child_node, action_list + [action], cards, action_prob * reach_probability_1 , reach_probability_2) 
        elif player == 1:
            utility[action] = - CFR_minimization(child_node, action_list + [action], cards,  reach_probability_1, action_prob * reach_probability_2) 

        total_utility += action_prob * utility[action]


    compute_regret(node, total_utility, utility)
    if player == 0:
        reach_probability = reach_probability_2
    else:
        reach_probability = reach_probability_1

    update_cumulative_regret(node, reach_probability)
    update_strategy(node, reach_probability) # really reach here?
    return total_utility    


def compute_regret(node, total_utility, utility):
    for i in range (0, len(utility)):
        node.regrets[i] = utility[i] - total_utility

def update_cumulative_regret(node, reach_probability):
    for i in range (0, len(node.cumulative_regrets)):
        node.cumulative_regrets[i] += reach_probability * node.regrets[i]

def update_strategy(node, realization_weight=1):
    strat_sum = 0
    for i in range (0, len(node.strategy)):
        node.strategy[i] = node.cumulative_regrets[i] if node.cumulative_regrets[i] > 0 else 0
        strat_sum += node.strategy[i]

    for i in range (0, len(node.strategy)):
        if strat_sum > 0:
            node.strategy[i] = node.strategy[i] / strat_sum
        else:
            node.strategy[i] = 1 / len(node.strategy)
        node.strategy_sum[i] += realization_weight * node.strategy[i]
    return

def compute_average_strategy(node):
    avg_strategy = [0,0]
    normalizing_sum = sum(node.strategy_sum)
    for i in range (0,len(node.strategy_sum)):
        if normalizing_sum > 0:
            avg_strategy[i] = node.strategy_sum[i] / normalizing_sum
        else:
            avg_strategy[i] = 1 / len(node.strategy_sum)
    return avg_strategy

      

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


def train(num_steps):
    for i in range(0, num_steps):
        cards = draw_cards()
        action_list = []
        node = get_node(action_list, cards)
        CFR_minimization(node,action_list, cards, 1, 1)


train(5000000)  

for node in node_dict.values():
    print ("Action lists:", node.action_list)
    print ("Card: ", node.card)
    print (node.strategy)
    print (compute_average_strategy(node))
    print ("\n")

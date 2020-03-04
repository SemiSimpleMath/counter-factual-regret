def prepare_pair(tuple1, tuple2):

    h1rank1, h1suit1 = tuple1[0]
    h1rank2, h1suit2 = tuple1[1]
        
    h2rank1, h2suit1 = tuple2[0]
    h2rank2, h2suit2 = tuple2[1]
        

            

           
    if h1suit1 == h1suit2:
        H1SUITED = True
    else:
        H1SUITED = False
        
    if h2suit1 == h2suit2:
        H2SUITED = True
    else:
        H2SUITED = False
            
    overlap = 0
        
    if h1suit1 == h2suit1:
        overlap +=1
    if h1suit1 == h2suit2:
        overlap +=1
    if h1suit2 == h2suit1:
        overlap += 1
    if h1suit2 == h2suit2:
        overlap += 1
        
    if not H1SUITED and not H2SUITED:
        if overlap == 0:
            h1suit1 = 1
            h1suit2 = 0
            h2suit1 = 3
            h2suit2 = 2
                
        elif overlap == 1:
            if h1suit1 == h2suit1:
                h1suit1 = 1
                h1suit2 = 0
                h2suit1 = 1
                h2suit2 = 2
            elif h1suit1 == h2suit2:
                h1suit1 = 1
                h1suit2 = 0
                h2suit1 = 2
                h2suit2 = 1
            elif h1suit2 == h2suit1:
                h1suit1 = 1
                h1suit2 = 0
                h2suit1 = 0
                h2suit2 = 2
            elif h1suit2 == h2suit2:
                h1suit1 = 1
                h1suit2 = 0
                h2suit1 = 2
                h2suit2 = 0
        elif overlap == 2:
            if h1suit1 == h2suit1:
                h1suit1 = 1
                h1suit2 = 0
                h2suit1 = 1
                h2suit2 = 0
            elif h1suit2 == h2suit1:
                h1suit1 = 1
                h1suit2 = 0
                h2suit1 = 0
                h2suit2 = 1             
    if H1SUITED and not H2SUITED:
        if overlap == 0:
            h1suit1 = 0
            h1suit2 = 0
            h2suit1 = 2
            h2suit2 = 1
        elif overlap == 2:
                if h1suit1 == h2suit1:
                    h1suit1 = 0
                    h1suit2 = 0
                    h2suit1 = 0
                    h2suit2 = 1
                elif h1suit1 == h2suit2:
                    h1suit1 = 0
                    h1suit2 = 0
                    h2suit1 = 1
                    h2suit2 = 0

    if H1SUITED and H2SUITED:
        if overlap == 0:
            h1suit1 = 0
            h1suit2 = 0
            h2suit1 = 1
            h2suit2 = 1
        if overlap == 4:
            h1suit1 = 0
            h1suit2 = 0
            h2suit1 = 0
            h2suit2 = 0
                
    if not H1SUITED and H2SUITED:
        if overlap == 0:
            h1suit1 = 1
            h1suit2 = 0
            h2suit1 = 2
            h2suit2 = 2
        elif overlap == 2:
                if h1suit1 == h2suit1:
                    h1suit1 = 1
                    h1suit2 = 0
                    h2suit1 = 1
                    h2suit2 = 1
                elif h1suit2 == h2suit1:
                    h1suit1 = 1
                    h1suit2 = 0
                    h2suit1 = 0
                    h2suit2 = 0
        
    return  ( ( (h1rank1,h1suit1), (h1rank2, h1suit2) ) , ( (h2rank1, h2suit1) , (h2rank2, h2suit2) ) )    
 
    


def put_hand_in_standard_form(hand):
    
    rank1 = hand[0][0]
    rank2 = hand[1][0]
    
    if rank2 > rank1:
        rank1,rank2 = rank2,rank1
    
    suit1 = hand[0][1]
    suit2 = hand[1][1]
    
    if suit1 == suit2:
        suit1, suit2 = 0,0
        
    if suit1 != suit2:
        suit1, suit2 = 1,0
        
    hand = ( (rank1,suit1), (rank2,suit2) )
    
    return hand




def calculate_pot_from_action_list(action_list):
    
    sb = 1
    bb=2
    pot = sb + bb
    
    amount_needed_to_call=[1,0]

    money_put_in = [1,2]
    
    amounts = []
    pots = []
    
    pots.append(pot)
    
    for i in range (0, len(action_list)):
        player = i % 2
        action = action_list[i]

        if action == 1:
            
            pot += amount_needed_to_call[player]
            amounts.append(amount_needed_to_call[player])
            
            money_put_in[player] += amount_needed_to_call[player]
            
            amount_needed_to_call[player] = 0  
            
            pots.append(pot)
            
        if action == 2:
            raise_amount =  2 * amount_needed_to_call[player] + pot
            pot += raise_amount
            
            money_put_in[player] += raise_amount
            
            amounts.append(raise_amount)


            amount_needed_to_call[(player + 1) % 2] = raise_amount - amount_needed_to_call[player]
            
            amount_needed_to_call[player] = 0
            pots.append(pot)
            
        if action == 3:
            raise_amount = 100 - money_put_in[player]
            amount_needed_to_call[(player + 1) % 2]  = 100 - money_put_in[(player+1) % 2]
            pot += raise_amount
            
            money_put_in[player] += raise_amount
            
            pots.append(pot)
        
    return (pots, amounts, money_put_in)
        

def order_cards(hand):
    hand1 = hand[0]
    hand2 = hand[1]
    if hand1[0] < hand2[0]:
        hand1, hand2 = hand2, hand1
        hand = (hand1, hand2)
    return hand


def generate_two_card_hands():
    #we order these so the first card is always higher rank (0,12)
    # suites are ordered (0,3)
    # we first order by rank then by suite
    
    hand_set = set()
    for rank1 in range (12,-1,-1):
        for rank2 in range (rank1, -1, -1):
            
            for suite1 in range (3,-1,-1):
                for suite2 in range (3,-1,-1):
                    fail = False
                
                ## check if the hand could be a poker hand
                ## cannot repeat suite for pairs
                
                    if rank1 == rank2 and suite1 == suite2:
                        fail = True
                    
                    a= suite1
                    b= suite2
                    
                    if rank1 == rank2 and suite1 < suite2:
#                        #swap suites
                         a= suite2
                         b= suite1
                    if not fail:
                        hand_set.add(((rank1,a),(rank2,b)))
    return hand_set
                    

def generate_hand_pairs():
    hs1 = generate_two_card_hands()
    hs2 = generate_two_card_hands()
    
    final_set = set()
    for hand1 in hs1:
        for hand2 in hs2:
            fail=False
            if (hand1[0] == hand2[0]) or (hand1[0] == hand2[1]) or (hand1[1] == hand2[0]) or (hand1[1] == hand2[1]):
                fail=True
            if not fail:
                final_set.add((hand1,hand2))
    return final_set



def generate_sf_list(hs):
    sf_set = set()
    for hand in hs:
        hand = put_hand_in_standard_form(hand)
        sf_set.add(hand)
    sf_list = list(sf_set)
    return sf_list
    


def order_hand(hand):
    card1 = hand[0]
    card2 = hand[1]

    if card1[0] < card2[0]:
        card1, card2 = card2,card1
        hand = (card1,card2)
    return hand

def adjust_pair_order(hand):
    card1, card2 = hand
    if card1[0] == card2[0]:
        if card1[1] < card2[1]:
            hand = (card2,card1)
    return hand
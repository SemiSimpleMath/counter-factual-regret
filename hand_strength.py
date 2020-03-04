
import cnfg
import hand_functions 

def look_up_hand_vs_hand(hand1, hand2):
    # hand1 and hand2 assumed to have been prepared to be compatible 
    key = (hand1,hand2)
    return cnfg.MCT[key]


def generate_expanded_sf_list(hand, hand2):
    
    card11 = hand[0]
    card12 = hand[1]
    
    card21 = hand2[0]
    card22 = hand2[1]
    
    rank1 = card11[0]
    rank2 = card12[0]
    
    suite1 = card11[1]
    suite2 = card12[1]
    
    c_list = []
    
    if suite1 != suite2 and rank1 != rank2:
        for i in range(3,-1,-1):
            for j in range (3, -1, -1):
                if i !=j:
                    c1=(rank1,i)
                    c2 = (rank2,j)
                    
                    if c1 !=card21 and c1 != card22 and c2 != card21 and c2!=card22:
                        c_list.append((c1,c2))
                        
                        
    if suite1 == suite2:
        for i in range (3,-1,-1):
            c1=(rank1,i)
            c2 = (rank2,i)
                    
            if c1 !=card21 and c1 != card22 and c2 != card21 and c2!=card22:
                c_list.append((c1,c2))
      
    if rank1 == rank2:
        
        for j in range (3,-1,-1):

            for i in range (j-1,-1,-1):
                c1 = (rank1, j)
                c2 = (rank1, i)

                h = (c1,c2)

                if c1 !=card21 and c1 != card22 and c2 != card21 and c2!=card22:
                    c_list.append(h)

            
        
        
        
    return c_list
 


### SF VS SF HAND STRENGTH

def generate_sf_hand_vs_sf_hand_table():
    for hand1 in cnfg.SF_LIST:
        for hand2 in cnfg.SF_LIST:
            total_wrt = 0
            total_ties = 0
            count = 0
            expanded_sf_list = generate_expanded_sf_list(hand2, hand1)
            weight = len(expanded_sf_list)
            for h2 in expanded_sf_list:
                hand1, h2 = hand_functions.prepare_pair (hand1, h2)
                wrt, ties, c = look_up_hand_vs_hand(hand1, h2)
                total_wrt +=wrt
                total_ties +=ties
                count +=1
            cnfg.SF_VS_SF[(hand1,hand2)] = (total_wrt/count,total_ties/count, weight)

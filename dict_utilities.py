
import json



def reverse_encode_string_to_pair_tupple(hands):

    
    h1rank1 = int(hands[0:2])
    h1suite1 = hands[2]
    h1rank2 = int(hands[3:5])
    h1suite2 = hands[5]

    h2rank1 = int(hands[6:8])
    h2suite1 = hands[8]
    h2rank2 = int(hands[9:11])
    h2suite2 = hands[11]
    
    suite_dict = dict({"C":0, "D":1 , "H":2, "S":3})
    
    h1suite1 = suite_dict[h1suite1]
    h1suite2 = suite_dict[h1suite2]
    
    h2suite1 = suite_dict[h2suite1]
    h2suite2 = suite_dict[h2suite2]
    
    tuple1 = ((h1rank1, h1suite1) , (h1rank2, h1suite2))
    tuple2 = ((h2rank1, h2suite1) , (h2rank2, h2suite2))
    
    return (tuple1,tuple2)


def load_mct_dict():
    import pickle
    infile = open("data/dicts/mct_dict2.p" ,'rb')
    MCT = pickle.load(infile)
    infile.close()

    return MCT
    #mct_string = json.load( open( "data/dicts/mct_dict.json" ) )
    #return create_mct_dict_from_mct_string(mct_string)

def create_mct_dict_from_mct_string(mct_string):
    MCT = dict()
    for key, value in mct_string.items():
        k = reverse_encode_string_to_pair_tupple(key)
        MCT[k]=value
    return MCT
    



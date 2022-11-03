import json
from operator import itemgetter


def get_role_given(Team_ID,Current_Score):
    #Reads the role points config from the config file.
    with open('config.json') as json_file:
          config = json.load(json_file)
    role_score_break = config['role_score_break']

    #Makes sure role is in descending order.
    role_score_break_sorted = sorted(role_score_break, key=itemgetter('Min'), reverse=True) 
    #Loops through roles and then sees if they above min, if so will return that role.
    for item in role_score_break_sorted :
        if Current_Score>= item['Min']:
            return item

    
    



import time
import json
import pandas as pd
import numpy as np

import call_data

account_ids = pd.read_csv('../data/account_ids.csv')
heroes = call_data.get_heroes()

# 1. Get match ids from each account

matches_mh =  call_data.get_data(account_ids['id'][0], heroes)
matches_shiri =  call_data.get_data(account_ids['id'][1], heroes)
matches_bacon =  call_data.get_data(account_ids['id'][2], heroes)
matches_mo =  call_data.get_data(account_ids['id'][3], heroes)
matches_bottle =  call_data.get_data(account_ids['id'][4], heroes)
matches_king =  call_data.get_data(account_ids['id'][5], heroes)
matches_deathcat =  call_data.get_data(account_ids['id'][6], heroes)
matches_boss =  call_data.get_data(account_ids['id'][7], heroes)

# 2. Get unique match_id from all account matches

match_ids = matches_mh['match_id'].tolist() \
    + matches_shiri['match_id'].tolist() \
    + matches_bacon['match_id'].tolist() \
    + matches_mo['match_id'].tolist() \
    + matches_bottle['match_id'].tolist() \
    + matches_king['match_id'].tolist() \
    + matches_deathcat['match_id'].tolist() \
    + matches_boss['match_id'].tolist()

match_ids = list(set(match_ids))

len(match_ids)
len(match_ids) / 60 / 60 # 3 hours @ 60 calls per minute

# 3. Loop through each match_id and make api call to match

match_ids[1]
match_ids[2]

match_id1 = 5440110597 # unranked, no lane_role
match_id2 = 581553375 # ranked, lane_role exists

# The data available in ranked/unranked roles are different.
match_1 = call_data.get_match(match_id=match_id1)
match_2 = call_data.get_match(match_id=match_id2)

for i in range(0, 60): 
    print(i)
    d[match_ids[i]] = call_data.get_match(match_id=match_ids[i])
    time.sleep(1) # sleep 1 second to ensure max 60 calls / minute



# 4. save to file

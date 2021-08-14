import time
import json

import call_data

# 1. Get match ids from each account

matches_mh =  get_data(account_ids['id'][0])
matches_shiri =  get_data(account_ids['id'][1])
matches_bacon =  get_data(account_ids['id'][2])
matches_mo =  get_data(account_ids['id'][3])
matches_bottle =  get_data(account_ids['id'][4])
matches_king =  get_data(account_ids['id'][5])
matches_deathcat =  get_data(account_ids['id'][6])
matches_boss =  get_data(account_ids['id'][7])

# 2. Get unique match_id from all account matches

match_ids = matches_mh.match_id.tolist() \
    + matches_shiri.match_id.tolist() \
    + matches_bacon.match_id.tolist() \
    +  matches_mo.match_id.tolist() \
    + matches_bottle.match_id.tolist() \
    + matches_king.match_id.tolist() \
    + matches_deathcat.match_id.tolist() \
    + matches_boss.match_id.tolist()

match_ids = list(set(match_ids))

len(match_ids)
len(match_ids) / 60 / 60 # 2.78416 hours @ 60 calls per minute

# 3. Loop through each match_id and make api call to match

match_0 = get_match(match_id=match_ids[0])
match_1 = get_match(match_id=match_ids[1])

d = {}
d[match_ids[0]] = match_0
d[match_ids[1]] = match_1
# d

for i in range(1000, 2000):
    print(i)
    d[match_ids[i]] = get_match(match_id=match_ids[i])
    time.sleep(1) # sleep 1 second to ensure max 60 calls / minute

len(d)
d

# 4. save to file

with open('data.json', 'w') as fp:
    json.dump(d, fp)
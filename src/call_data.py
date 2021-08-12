import requests
import json
import pandas as pd
import numpy as np

api_key = '?api_key=' + key

end_path = 'players/208812212/'

url = host_name + end_path + api_key

url

response = requests.get(url)

response

response.text

pretty_json = json.loads(response.text)
print(json.dumps(pretty_json, indent=4))

url = host_name + end_path + 'matches/' + api_key

r = requests.get(url)
matches_data = json.loads(r.text)

df = pd.DataFrame(matches_data)
df

df.to_csv('data/data.csv')




# Heroes
# Should run only once; placed in __name__
def get_heroes():
    url = host_name + 'heroes'
    r = requests.get(url)
    heroes = json.loads(r.text)
    return(heroes)

# Test
# heroes = get_heroes()

# Get all the matches, given an ID
def get_player_matches(account_id, api_key=api_key):
    # Gets only all-pick matches (game_mode=22)
        
    url = host_name \
        + 'players/' \
        + account_id \
        + '/matches/' \
        + '?api_key=' \
        + api_key \
        + '?game_mode=22' \
        + '?limit=500'
    
    r = requests.get(url)
    data = json.loads(r.text)
    
    return(data)

# Test
matches = get_player_matches(account_id='208812212')
matches[0]

# Match data should only be called once, especially when in a party
# TODO: Maybe turn this into a class so attributes can be accessed more easily
def get_match(match_id, api_key=api_key):
    url = host_name \
        + 'matches/' \
        + str(match_id) \
        + '?api_key=' \
        + api_key \
    
    r = requests.get(url)
    data = json.loads(r.text)
    
    return(data)

# test
match = get_match(match_id=6130305670)
match
match['players']
match['players'][0]['match_id']
match['players'][0]['player_slot']
match['players'][0]['account_id']
match['players'][0]['lane']
match['players'][0]['lane_role']
match['players'][0]['win'] # Another way to determine win/loss
match['players'][0]['lose']

class Match:
    '''Match class'''
    
    def __init__(self, match_id):
        self.match_id = match_id
        self.data = get_match(self.match_id)
    
    
match = Match(6130305670)
match.match_id
match.data

# Extract data for each player
matches = get_player_matches(account_id='208812212') # mh
# matches = get_player_matches(account_id='156306162') # shiri
# matches = get_player_matches(account_id='1075655293') # bacon
# matches = get_player_matches(account_id='152471066') # mo
# matches = get_player_matches(account_id='1075592541') # bottle
# matches = get_player_matches(account_id='125430576') # king
# matches = get_player_matches(account_id='103619307') # deathcat

# This merges data together
(
    pd.DataFrame(matches)
    .merge(
        pd.DataFrame(heroes)[['id', 'localized_name']], 
        left_on='hero_id', 
        right_on='id'
        )
    .rename(columns={'localized_name': 'hero'})
    .assign(team=lambda x: np.where(x['player_slot'] <= 5, 'radiant', 'dire'),
            win=lambda x: np.where(x['team'] == 'radiant', x['radiant_win'], x['radiant_win'] == False))
    .drop(columns=[
        'id', 'hero_id', 'game_mode', 
        'lobby_type', 'leaver_status', 'skill',
        'player_slot', # used to merge other match data
        'radiant_win', 'version'
        ])
    # .to_csv('./data/matches_mh.csv', index=False)
    # .to_csv('./data/matches_shiri.csv', index=False)
    # .to_csv('./data/matches_bacon.csv', index=False)
    # .to_csv('./data/matches_mo.csv', index=False)
    # .to_csv('./data/matches_bottle.csv', index=False)
    # .to_csv('./data/matches_king.csv', index=False)
    # .to_csv('./data/matches_deathcat.csv', index=False)
)

def lane_role(lane_role):
    if (lane_role == 0): return("unknown")
    elif (lane_role == 1): return("safe")
    elif (lane_role == 2): return("mid")
    elif (lane_role == 3): return("off")

# Test
# lane_role(lane_role=1)

if __name__ == '__main__':
    
    print('Executing as standalone script')
    
    ids = pd.read_csv('data/player_ids.csv')
    
    api_key = open('keys.txt', 'r').read()
    
    host_name = 'https://api.opendota.com/api/'
    
    heroes = get_heroes()
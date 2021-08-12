import requests
import json
import pandas as pd
import numpy as np

player_ids = pd.read_csv('../data/player_ids.csv')

# api_key = '?api_key=' + key

# end_path = 'players/208812212/'

# url = host_name + end_path + api_key

# url

# response = requests.get(url)

# response

# response.text

# pretty_json = json.loads(response.text)
# print(json.dumps(pretty_json, indent=4))

# url = host_name + end_path + 'matches/' + api_key

# r = requests.get(url)
# matches_data = json.loads(r.text)

# df = pd.DataFrame(matches_data)
# df

# df.to_csv('data/data.csv')




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
        + str(account_id) \
        + '/matches/' \
        + '?api_key=' \
        + api_key \
        + '?game_mode=22'
    
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
# matches = get_player_matches(account_id='208812212') # mh
# matches = get_player_matches(account_id='156306162') # shiri
# matches = get_player_matches(account_id='1075655293') # bacon
# matches = get_player_matches(account_id='152471066') # mo
# matches = get_player_matches(account_id='1075592541') # bottle
# matches = get_player_matches(account_id='125430576') # king
matches = get_player_matches(account_id='103619307') # deathcat
# matches = get_player_matches(account_id='100501459') # boss

# This merges data together
(
    pd.DataFrame(matches)
    .merge(
        pd.DataFrame(heroes)[['id', 'localized_name']], 
        left_on='hero_id', 
        right_on='id'
        )
    .rename(columns={'localized_name': 'hero'})
    .sort_values(['start_time'])
    .assign(team=lambda x: np.where(x['player_slot'] <= 5, 'radiant', 'dire'),
            win=lambda x: np.where(x['team'] == 'radiant', x['radiant_win'], x['radiant_win'] == False))
    .assign(avg_win_rate_20=lambda x: x['win'].rolling(window=20).mean())
    .drop(columns=[
        'id', 
        'hero_id', 
        'game_mode', 
        'lobby_type', 
        'leaver_status', 
        'skill',
        'player_slot', # used to merge other match data
        'radiant_win', 'version'
        ])
)

def get_data(account_id):
    matches = get_player_matches(account_id)
    
    matches = (
        pd.DataFrame(matches)
        .merge(
            pd.DataFrame(heroes)[['id', 'localized_name']], 
            left_on='hero_id', 
            right_on='id'
            )
        .rename(columns={'localized_name': 'hero'})
        .sort_values(['start_time'])
        .assign(team=lambda x: np.where(x['player_slot'] <= 5, 'radiant', 'dire'),
                win=lambda x: np.where(x['team'] == 'radiant', x['radiant_win'], x['radiant_win'] == False))
        .assign(avg_win_rate_20=lambda x: x['win'].rolling(window=20).mean(),
                avg_kills_20=lambda x: x['kills'].rolling(window=20).mean(),
                avg_deaths_20=lambda x: x['deaths'].rolling(window=20).mean(),
                avg_assists_20=lambda x: x['assists'].rolling(window=20).mean())
        .drop(columns=[
            'id', 
            'hero_id', 
            'game_mode', 
            'lobby_type', 
            'leaver_status', 
            'skill',
            'player_slot', # used to merge other match data
            'radiant_win', 'version'
            ])
    )
    
    return(matches)

# test
# matches_df = get_data(account_ids['id'][0])

def get_and_save_data(account_id, alias):
    
    matches_df = get_data(account_id)

    location = '../data/matches_' + alias + '.csv'
    matches_df.to_csv(location, index=False)

# test
# get_and_save_data(account_id=account_ids['id'][0], alias=account_ids['name'][0])

# Get and save data for all account ids
for i in range(account_ids.shape[0]):
    get_and_save_data(account_ids['id'][i], account_ids['name'][i])


def lane_role(lane_role):
    if (lane_role == 0): return("unknown")
    elif (lane_role == 1): return("safe")
    elif (lane_role == 2): return("mid")
    elif (lane_role == 3): return("off")

# Test
# lane_role(lane_role=1)

if __name__ == '__main__':
    
    print('Executing as standalone script')
    
    account_ids = pd.read_csv('../data/account_ids.csv')
    
    api_key = open('../keys.txt', 'r').read()
    
    host_name = 'https://api.opendota.com/api/'
    
    heroes = get_heroes()
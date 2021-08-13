import requests
import json
import pandas as pd
import numpy as np

account_ids = pd.read_csv('../data/account_ids.csv')

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
        + api_key
    
    r = requests.get(url)
    data = json.loads(r.text)
    
    return(data)

# test = get_player_matches(account_id=account_id)
# test

# Match data should only be called once, especially when in a party
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
match['lobby_type']
match['patch']
match['region']

# Data within each player
match['players']
match['players'][0]['match_id']
match['players'][0]['player_slot']
match['players'][0]['account_id']
match['players'][0]['lane']
match['players'][0]['lane_role']
match['players'][0]['win'] # Another way to determine win/loss
match['players'][0]['lose'] # Another way to determine win/loss

def extract_match_player_stats(match, player=0):
    
    match_player_data = match['players'][player]
    

class Match:
    '''Match class'''
    
    def __init__(self, match_id):
        self.match_id = match_id
        self.data = get_match(self.match_id)
    
    
match = Match(6130305670)
match.match_id
match.data

def get_data(account_id):
    matches = get_player_matches(account_id)
    
    matches = (
        pd.DataFrame(matches)
        .merge(
            pd.DataFrame(heroes)[['id', 'localized_name']], 
            left_on='hero_id', 
            right_on='id'
            )
        .query('game_mode == 22 | game_mode == 1 | game_mode == 23')
        .rename(columns={'localized_name': 'hero'})
        .sort_values(['start_time'])
        .assign(team=lambda x: np.where(x['player_slot'] <= 5, 'radiant', 'dire'),
                win=lambda x: np.where(x['team'] == 'radiant', x['radiant_win'], x['radiant_win'] == False),
                ranked=lambda x: np.where(x['lobby_type'] == 7, 1, 0))
        .assign(avg_win_rate_20=lambda x: x['win'].rolling(window=20).mean(),
                avg_kills_20=lambda x: x['kills'].rolling(window=20).mean(),
                avg_deaths_20=lambda x: x['deaths'].rolling(window=20).mean(),
                avg_assists_20=lambda x: x['assists'].rolling(window=20).mean(),
                max_kills_20=lambda x: x['kills'].rolling(window=20).max(),
                max_deaths_20=lambda x: x['deaths'].rolling(window=20).max(),
                max_assists_20=lambda x: x['assists'].rolling(window=20).max())
        .drop(columns=[
            'id', 
            'hero_id', 
            # 'game_mode', 
            'lobby_type', 
            'leaver_status', 
            'skill',
            'player_slot', # used to merge other match data
            'radiant_win', 'version'
            ])
    )
    
    matches['win'] = matches['win'].apply(lambda x: int(x))
    
    return(matches)

# test
matches_df = get_data(account_ids['id'][1])
matches_df
# matches_df['party_size'].value_counts()
# matches_df.ranked.value_counts()
# matches_df['win'].value_counts()
matches_df['game_mode'].value_counts()

def get_and_save_data(account_id, alias):
    
    matches_df = get_data(account_id)

    location = '../data/matches_' + alias + '.csv'
    matches_df.to_csv(location, index=False)

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
import requests
import json
import pandas as pd

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

# Get all the matches, given an ID


# Heroes
def get_heroes():
    url = host_name + 'heroes'
    r = requests.get(url)
    heroes = json.loads(r.text)
    return(heroes)

# Test

def get_matches(account_id, api_key = api_key):
    
    # Only want normal all-pick matches:
    # 1: game_mode_all_pick
    # 22: game_mode_all_draft <- Most matches are 22 for some reason
    
    url = host_name \
        + 'players/' \
        + account_id \
        + '/matches/' \
        + '?api_key=' + api_key \
        + '?game_mode=22'
    
    r = requests.get(url)
    data = json.loads(r.text)
    
    return(data)

# Test
matches = get_matches(account_id='208812212')
len(matches)
matches[0]
matches[-1]
    


if (__name__ == '__main__'):
    
    print('Executing as standalone script')
    
    import requests
    import json
    
    ids = pd.read_csv('data/player_ids.csv')
    
    api_key = open('keys.txt', 'r').read()
    
    host_name = 'https://api.opendota.com/api/'
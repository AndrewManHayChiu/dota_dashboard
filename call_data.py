import requests
import json
import pandas as pd

key = open('keys.txt', 'r').read()

host_name = 'https://api.opendota.com/api/'

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

def get_matches(account_id):
    
    url = host_name + 'players/' + str(account_id) + '/matches/' + api_key
    
    response = requests.get(url)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    
    return(df)
    
get_matches(account_id=208812212)

def get_match(match_id):
    
    url = host_name + 'matches/' + str(match_id) + api_key
    
    response = requests.get(url)
    data = json.loads(response.text)
    # df = pd.DataFrame(data)
    
    return pd.DataFrame(data)

get_match(6064493671)

# def save_data(file_name):
    

# def update_data():
    
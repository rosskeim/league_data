import requests, json
import pandas as pd

account = "bEEDcwc6ohmom9qBAJM7fHav5nSxp8H2E-Tfvf4iofQI0w"
api_key = "RGAPI-1e5772b3-a66c-4cff-b7f3-7e12bea7b045"

response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account + "?api_key=" + api_key)

data = response.json()

df = pd.DataFrame(data['matches'])
games = df['gameId'].values.tolist()

record = []
wins = 0
losses = 0

for x in range(1):
    response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + str(games[x]) + "?api_key=" + str(api_key))
    data = response.json()
    print(data.keys())
    for y in data['participantIdentities']:
        if(y['player']['currentAccountId'] == account):
            part = y['participantId']
    for z in data['participants']:
        if z['participantId'] == part:
            print(z['participantId']['stats']['win'])

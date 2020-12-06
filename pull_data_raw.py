import requests, json
import pandas as pd

account = "bEEDcwc6ohmom9qBAJM7fHav5nSxp8H2E-Tfvf4iofQI0w"
api_key = "RGAPI-2ec937e8-a268-4a61-9fb2-acbe514a7c26"

response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account + "?api_key=" + api_key)

data = response.json()

df = pd.DataFrame(data['matches'])
games = df['gameId'].values.tolist()

record = []
current = 0
wins = 0
losses = 0

x = 1 
while x <= 10:
  response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + str(games[x]) + "?api_key=" + str(api_key))
  data = response.json()
  for y in data['participantIdentities']:
    if(y['player']['currentAccountId'] == account):
      part = y['participantId']
      for z in data['participants']:
        if z['participantId'] == part:
          print("#" + str(games[x]) + ": " + str(z['timeline']['role']) + " " + str(z['timeline']['lane']) + " champion(" + str(z['championId']) + ") Win: " + str(z['stats']['win'])) 
          if z['stats']['win'] == True:
            wins += 1
          else:
            losses += 1
  current = x
  x = x + 1

print("==========RESULTS==========")
print("Games: " + str(current))
print("Wins: " + str(wins))
print("Losses: " + str(losses))

import requests, json
import pandas as pd
import datetime

account = "bEEDcwc6ohmom9qBAJM7fHav5nSxp8H2E-Tfvf4iofQI0w"
api_key = "RGAPI-e68f6cde-c59e-4776-b80e-6d0cb90e8ec2"

############### LOAD CHAMPION DICT ##################
with open('champion.json') as f:
  data = json.load(f)
  champ_dict = {}

for k,v in data['data'].items():
  champ_dict[int(v['key'])] = k
#####################################################

response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account + "?api_key=" + api_key)

data = response.json()

df = pd.DataFrame(data['matches'])
games = df['gameId'].values.tolist()

record = []
current = 0
wins = 0
losses = 0

print("Enter number of games: ")
num = int(input())

x = 1 
while x <= num:
  response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + str(games[x]) + "?api_key=" + str(api_key))
  data = response.json()
  for y in data['participantIdentities']:
    if(y['player']['currentAccountId'] == account):
      part = y['participantId']
      for z in data['participants']:
        if z['participantId'] == part:
          duration = float(data['gameDuration']/60)
          dpm = round(z['stats']['deaths']/duration, 2)
          gpm =  round(z['stats']['goldEarned']/duration, 2)
          cpm = round(z['stats']['totalMinionsKilled']/duration, 2)
          print("#" + str(games[x]), end="-")
          print(str(data['gameCreation']), end=":")
          print(str(z['timeline']['role']) + " " + str(z['timeline']['lane']), end=" ")
          print(str(champ_dict[int(z['championId'])]) + " Win: " + str(z['stats']['win']), end=" ")
          print("DPM: " + str(dpm) + " GPM: " + str(gpm) + " CPM: " + str(cpm)) 
          if z['stats']['win'] == True:
            wins += 1
          else:
            losses += 1
  current = x
  x = x + 1

print("====================RESULTS====================")
print("Games: " + str(current))
print("Wins: " + str(wins))
print("Losses: " + str(losses))
print("Winrate: " + str(wins/current))

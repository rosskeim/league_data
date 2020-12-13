import requests, json
import pandas as pd
import datetime
import time

account = "bEEDcwc6ohmom9qBAJM7fHav5nSxp8H2E-Tfvf4iofQI0w"
api_key = "RGAPI-d3c3a3e8-0b24-4f44-bd57-0f5e196c4db0"

############### LOAD CHAMPION DICT ##################
with open('champion.json', encoding='utf-8') as f:
  data = json.load(f)
  champ_dict = {}

for k,v in data['data'].items():
  champ_dict[int(v['key'])] = k
#####################################################

response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account + "?api_key=" + api_key)

data = response.json()

df = pd.DataFrame(data['matches'])
df.sort_values(by='timestamp', ascending=False)
print(df['gameId'])
games = df['gameId'].values.tolist()

record = []
current = 0
wins = 0
losses = 0

print("Enter number of games: ")
num = int(input())

matchdata = []

for i in games:

  response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + str(i) + "?api_key=" + str(api_key))
  time.sleep(2)
  response_f = response.json()
  print(response_f)
  rawtime = response_f['gameCreation']
  timestamp = datetime.datetime.fromtimestamp(int(rawtime/1000)) 
  gametime = timestamp.strftime('%d/%m/%Y %H:%M:%S')
  duration = float(response_f['gameDuration']/60)

  for y in response_f['participantIdentities']:
    if(y['player']['currentAccountId'] == account):
      part = y['participantId']
      for z in response_f['participants']:
        if z['participantId'] == part:
          role = z['timeline']['role']
          lane = z['timeline']['lane']
          champ = champ_dict[int(z['championId'])]
          win = z['stats']['win']
          dpm = round(z['stats']['deaths']/duration, 2)
          gpm =  round(z['stats']['goldEarned']/duration, 2)
          cpm = round(z['stats']['totalMinionsKilled']/duration, 2)
          matchdata.append([gametime, role, lane, champ, win, duration, dpm, gpm, cpm])
          break
match_df = pd.DataFrame(matchdata, columns=['gametime', 'role', 'lane', 'champ', 'win', 'duration', 'dpm', 'gpm', 'cpm'])
match_df.to_csv('history.csv')

print(match_df)

"""
print("====================RESULTS====================")
print("Games: " + str(num))
print("Wins: " + str(wins))
print("Losses: " + str(losses))
print("Winrate: " + str(wins/num))
with open('history.csv', 'w') as p:
    for item in output:
        p.write("%s\n" % item)
"""
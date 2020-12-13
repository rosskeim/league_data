import requests, json
import pandas as pd
import datetime

account = "bEEDcwc6ohmom9qBAJM7fHav5nSxp8H2E-Tfvf4iofQI0w"
api_key = "RGAPI-8b0698d3-9a3f-447d-b666-dedeb28d662f"

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

output = {}
responses = []

for i in games:

  response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + str(i) + "?api_key=" + str(api_key))
  output[i] = response.json()
  output = sorted(output.items(), key=operator.itemgetter(1), reverse=True)

  for o in output.items():

  
    rawtime = r['gameCreation']
    timestamp = datetime.datetime.fromtimestamp(int(rawtime/1000)) 
    gametime = timestamp.strftime('%d/%m/%Y %H:%M:%S')
    output.append(gametime)

    for y in r['participantIdentities']:
      if(y['player']['currentAccountId'] == account):
        part = y['participantId']
        for z in r['participants']:
          if z['participantId'] == part:
            duration = float(r['gameDuration']/60)
            dpm = round(z['stats']['deaths']/duration, 2)
            gpm =  round(z['stats']['goldEarned']/duration, 2)
            cpm = round(z['stats']['totalMinionsKilled']/duration, 2)
            print("#" + str(games[i]), end="-")
            
            print(str(gametime), end=":")
            print(str(z['timeline']['role']) + " " + str(z['timeline']['lane']), end=" ")
            print(str(champ_dict[int(z['championId'])]) + " Win: " + str(z['stats']['win']), end=" ")
            print("DPM: " + str(dpm) + " GPM: " + str(gpm) + " CPM: " + str(cpm)) 
            if z['stats']['win'] == True:
              wins += 1
            else:
              losses += 1

print("====================RESULTS====================")
print("Games: " + str(num))
print("Wins: " + str(wins))
print("Losses: " + str(losses))
print("Winrate: " + str(wins/num))

with open('history.csv', 'w') as p:
    for item in output:
        p.write("%s\n" % item)

import requests, json
import pandas as pd
from pandas.plotting import scatter_matrix
from pandas.plotting import boxplot
from tabulate import tabulate
from pandas.io.json import json_normalize

account = "bEEDcwc6ohmom9qBAJM7fHav5nSxp8H2E-Tfvf4iofQI0w"
api_key = "RGAPI-1426ffcc-2ee9-4584-8a39-1a3baa3831bd"

response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + account + "?api_key=" + api_key)

data = response.json()
print(data)

df = pd.DataFrame(data['matches'])
games = df['gameId'].values.tolist()

record = []
wins = 0
losses = 0

for x in range(5):
	response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + str(games[x]) + "?api_key=" + str(api_key))
	data = response.json()
	print(data)

#response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matches/" + str(matches[1]) + "?api_key=" + api_key)
#data = response.json()

#for p in data['participantIdentities']:
#	if p['player']['currentAccountId'] == 'bEEDcwc6ohmom9qBAJM7fHav5nSxp8H2E-Tfvf4iofQI0w':
#		part = p['participantId']

#for y in data['participants']:
#	if y['participantId'] == part:
#		#result = y['win']
#		print(result)

#print(result)

from pantheon import pantheon
import asyncio

#import requests, json
#import pandas as pd

#response = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/bEEDcwc6ohmom9qBAJM7fHav5nSxp8H2E-Tfvf4iofQI0w?api+key=RGAPI-faa81865-a445-4b75-b82d-1c4785b59ff4")

#data = response.json()

server = "na1"
api_key = "RGAPI-faa81865-a445-4b75-b82d-1c4785b59ff4"

def requestsLog(url, status, headers):
	print(url)
	print(status)
	print(headers)

panth = pantheon.Pantheon(server, api_key, errorHandling=True, requestsLoggingFunction=requestsLog, debug=True)

async def getSummonerId(name):
	try:
		data = await panth.getSummonerByName(name)
		return (data['id'], data['accountId'])
	except Exception as e:
		print(e)


async def getRecentMatchlist(accountId):
	try:
		data = await panth.getMatchlist(accountId, params={"endIndex":10})
		return data
	except Exception as e:
		print(e)

async def getRecentMatches(accountId):
	try:
		matchlist = await getRecentMatchlist(accountId)
		tasks = [panth.getMatch(match['gameId']) for match in matchlist['matches']]
		return await asyncio.gather(*tasks)
	except Exception as e:
		print(e)

name = "Lonnie Childs"

loop = asyncio.get_event_loop()

(summonerId, accountId) = loop.run_until_complete(getSummonerId(name))
print(summonerId)
print(accountId)
print(loop.run_until_complete(getRecentMatches(accountId)))

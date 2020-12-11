import json

with open('champion.json') as f:
  data = json.load(f)

champ_dict = {}

for k,v in data['data'].items():
  champ_dict[int(v['key'])] = k

print(champ_dict)

import json

file = 'Clearbit_Demo.json'
fhand = open(file)
text = fhand.read()
data = json.loads(text)

for item in data['tech']:
	print(item)

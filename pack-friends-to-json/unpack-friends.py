import json

f = open("namesjson.txt", "r")
names = json.loads(f.read())
f.close()

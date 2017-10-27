## JSON to friends (dictionary reader)
## @author Ryan Pope
import json

f = open("namesjson.txt", "r")
names = json.loads(f.read())
f.close()

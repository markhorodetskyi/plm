import json

with open("settings.json", "r") as read_file:
    data = json.load(read_file)
print(data[0]['id'])

import requests
import json

url = "https://michaelgathara.com/api/python-challenge"

response = requests.get(url)

challenges =response.json()
# print(challenges)
print("name - Vijeth venkatesha \nBlazerID - vvenkate")
for i in challenges:
    solved= eval(i['problem'].replace("?",""))
    print(i['problem'].replace("?",""), "=", solved)


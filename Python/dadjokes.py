import requests

url = "https://icanhazdadjoke.com/search"

print("Welcome to DadJoke 3000")
theme = input("What kind of joke do you want to hear about? ")

response = requests.get(url, headers={"Accept": "Application/json"}, params={"term": theme})

data = response.json()
results = data["results"]
if results == []:
    print("Sorry, no jokes for that.")
else:
    for res in results:
        print(res["joke"])
        repeat = input("Wanna hear another one? [Yes/No]").lower()[0]
        if repeat == "n":
            break
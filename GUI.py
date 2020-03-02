import TournamentTop8
import eel
import json

eel.init('web', allowed_extensions=['.js', '.html'])


@eel.expose
def pull_challonge(user, key, url):
    TournamentTop8.challonge_top8_export(user,key,url)

@eel.expose
def parse_manual(myList = [], *args):
    matches = 10
    vals = 5
    data = []
    for x in range(0,matches):
        item = {"id": myList[x*vals]}
        item["player1"] = myList[(x*vals)+1]
        item["player2"] = myList[(x*vals)+2]
        item["p1Score"] = myList[(x*vals)+3]
        item["p2Score"] = myList[(x*vals)+4]
        item["winner"] = "" #might use later, but atm i have no use for finding the winner
        data.append(item)
    with open('data.json','w') as outfile:
        json.dump(data,outfile)

eel.start('main.html')

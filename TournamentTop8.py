import challonge
import math
import json
import pprint
#zdmtYhsDLrRqNxhS5qAb3KJHasOIAk0noIQRAz4I

def challonge_top8_export(username, key, url):
    challonge.set_credentials(username, key)

    #Format for t_url is the end of the url for challonge
    #If using a team, different format
    #https://newchallenger.challonge.com/SFV_NA_S6T7 uses format newchallenger-SFV_NA_S6T7 or team-tournamentid
    #otherwise https://challonge.com/wlcsmash1 uses format wlcsmash1 or tournamentid
    t_url = url

    tournament = challonge.tournaments.show(t_url)
    participants = challonge.participants.index(tournament["id"])
    matches = challonge.matches.index(tournament["id"])

    player_count = len(participants)
    # Number of rounds = ceiling(log2(numEntrants))
    # Number of matches per round = (numEntrants) / 2
    #This gives us the total number of winners rounds (Not Including GF) and we subtract 1 to get to start of top 8
    top8W_start = math.ceil(math.log2(player_count)) - 1

    #This is basically the challonge formula for finding the total number of rounds needed (not including GF) minus the total number of winners round
    #this gives us the total number of losers rounds, so we subtract 3 t oget the start of top 8
    #Didn't work, resorting to the original search for farthest round for losers side since GF wont affect it
    #top8L_start = -1 * (2 * (math.ceil(math.log2(player_count))) + math.floor((player_count/(2 * math.ceil(math.log2(player_count)))+.25)) - 1 - top8W_start + 1 - 5)

    #for t in matches:
    #    if t["round"] > highest_round:
    #        highest_round = t["round"]

    lowest_round = 0
    for t in matches:
        if t["round"] < lowest_round:
            lowest_round = t["round"]
    top8L_start = lowest_round + 3

    #Once it found the highest and lowest round values, subtract/add values to get all top 8 matches

    player1 = ""
    player2 = ""
    score1 = 0
    score2 = 0
    winner = ""
    first_ws = True
    first_l8 = True
    first_lq = True

    def isTop8(r):
        #if range is in top 8, return true
        if r >= top8W_start:
            return True
        elif r <= top8L_start:
            return True
        else:
            return False

    data = [] #json output
    for t in matches:

        #skips if not top 8
        if not isTop8(t["round"]):
            continue

        for i in participants:
            if t["player1-id"] == i["id"]:
                #sets player1 as name if provided (the one either entered in with no account or nickname for specific event)
                #if no name is found, uses the username
                if i["name"] is None:
                    player1 = i["username"]
                else:
                    player1 = i["name"] 

            if t["player2-id"] == i["id"]:
                if i["name"] is None:
                    player2 = i["username"]
                else:
                    player2 = i["name"] 

            if t["winner-id"] == i["id"]:
                if i["name"] is None:
                    winner = i["username"]
                else:
                    winner = i["name"] 

        scores = str(t["scores-csv"]).split('-')
        if t["scores-csv"] is None:
           # score1 = 0
           # score2 = 0
           pass
        else:
            score1 = scores[0]
            score2 = scores[1]
    
       # outputs all parsed values
        match_name = ""
        def round_switch(arg):
            switcher = {
                top8W_start:"ws",
                (top8W_start + 1): "wf",
                (top8W_start + 2): "gf",
                (top8L_start): "l8",
                (top8L_start - 1):"lq",
                (top8L_start - 2):"ls",
                (top8L_start - 3):"lf"
                }
            return switcher.get(arg,"er")
    
        r = round_switch((t["round"]))
        #print(r)
        pos = 1
        if (r == "ws" and first_ws):
            first_ws = False
        elif r == "ws" and not first_ws:
            pos = 2
        elif r == "l8" and first_l8:
            first_l8 = False
        elif r == "l8" and not first_l8:
            pos = 2
        elif r == "lq" and first_lq:
            first_lq = False
        elif r == "lq" and not first_lq:
            pos = 2

        #print(pos)
        #print(t["id"])
        #print(str(player1) + " vs " + str(player2))
        #print(str(score1) + " to " + str(score2))
        #print("Winner: " + str(winner))
        #print("")

        #json output for each match appended to data
        item = {"id": r +"_"+ str(pos)}
        item["player1"] = player1
        item["player2"] = player2
        item["p1Score"] = score1
        item["p2Score"] = score2
        item["winner"] = winner
        data.append(item)


        player1 = ""
        player2 = ""
        score1 = ""
        score2 = ""
        winner = ""


    with open('data.json', 'w') as outfile:
        json.dump(data,outfile)
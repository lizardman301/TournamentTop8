#this was a simple script just to output html and css for my template bracket
rounds = ["ws_1","ws_2","l8_1","l8_2","wf_1","lq_1","lq_2","ls_1","lf_1","gf_1"]
players = ["p1", "p2"]
left_names = [53, 53, 53, 53, 561, 561, 561,1006, 1471, 1471]
top_names = [83, 358, 595, 898, 221, 595, 898, 746, 746, 221]

f = open("html_stuff.txt","w+")

for x in rounds:
    for y in players:
        f.write('<span id="'+ x + '_' + y + '_score" class="scores">1</span>\n')
        f.write('<span id="'+ x + '_'  + y + '_name" class="names">test</span>\n')

f.write("-----------------------------------------------------------\n")

i = 0
for x in rounds:
    for y in players:
        f.write('#'+x+'_'+y+'_name{\n')
        f.write('\tleft: ' + str(left_names[i]) +'px;\n')
        if y == "p1":
            f.write('\ttop: ' + str(top_names[i]) +'px;\n')
        else:
            f.write('\ttop: ' + str(top_names[i] + 51) +'px;\n')
        f.write('}\n')

        f.write('#' + x + '_' + y + '_score{\n')
        f.write('\tleft: ' + str(left_names[i] + 399) +'px;\n')
        if y == "p1":
            f.write('\ttop: ' + str(top_names[i] + 6) +'px;\n')
        else:
            f.write('\ttop: ' + str(top_names[i] + 57) +'px;\n')
        f.write('}\n')
    i+=1


import csv

from matplotlib import projections



def get_first_rosters():
    plyrs = []
    with open('output_files/Final_Roster_2022-06-20 08:34:48.928794.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                qb = row[0]
                rb1 = row[1]
                rb2 = row[2]
                wr1 = row[3]
                wr2 = row[4]
                wr3 = row[5]
                te = row[6]
                fx = row[7]
                dst = row[8]
                budget = row[9]
                projection = row[10]
                plyrs.append([qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection])
                
            line_count += 1    
    return plyrs


def get_second_rosters():
    plyrs = []
    with open('output_files/Final_Roster.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                qb = row[0]
                rb1 = row[1]
                rb2 = row[2]
                wr1 = row[3]
                wr2 = row[4]
                wr3 = row[5]
                te = row[6]
                fx = row[7]
                dst = row[8]
                budget = row[9]
                projection = row[10]
                plyrs.append([qb, rb1, rb2, wr1, wr2, wr3, te, fx, dst, budget, projection])
                
            line_count += 1    
    return plyrs

def find_number_players(plyr1, plyr2, plyr3, plyr4, plyr5, plyr6):
    count1 = []
    count2 = []
    for element in first_csv:
        if plyr1 == element[0] and plyr2 == element[1] and plyr3 == element[4] and plyr4 == element[6] and plyr5 == element[8] and plyr6 == element[7]:
            count1.append(element)
    for element in second_csv:
        if plyr1 == element[0] and plyr2 == element[1] and plyr3 == element[4] and plyr4 == element[6] and plyr5 == element[8] and plyr6 == element[7]:
            count2.append(element)
    
    return [count1, count2]

def find_flex_count(plyr1):
    count1 = []
    count2 = []
    for element in first_csv:
        if plyr1 == element[7][:2]:
            count1.append(element)
    for element in second_csv:
        if plyr1 == element[7][:2]:
            count2.append(element)
    
    return [count1, count2]

def find_te_diff(te, fx):
    count1 = []
    count2 = []
    for element in first_csv:
        if te == element[6] and fx == element[7]:
            count1.append(element)
    for element in second_csv:
        if te == element[6] and fx == element[7]:
            count2.append(element)
    
    return [count1, count2]
 

def write_file(list, name):
    with open('generated_files/' + name + '.csv', 'w') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE', 'fx', 'dst', 'budget', 'projection'])

        # write multiple rows
        writer.writerows(list)
    


first_csv = get_first_rosters()
second_csv = get_second_rosters()
#players = find_number_players("QB1", "RB4", "WR15", "TE3", "DST1", "TE6")
#flex_count = find_flex_count("TE")
te_diff = find_te_diff("TE2", "TE3")
print(len(te_diff[0]))
print(len(te_diff[1]))

# first_list = players[0]
# second_list = players[1]
# write_file(first_list, 'first_list')
# write_file(second_list, 'second_list')


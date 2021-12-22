#Player 1 starting position: 7
#Player 2 starting position: 5

p1_loc = 7
p2_loc = 5

p1_score = 0
p2_score = 0

die = 1
die_roll =0

def p1():
    while p1_score < 1000 and p2_score <1000:
        #p1 move
        p1_move = 0
        for i in range(3):
            die_roll += 1
            p1_move +=die
            die+=1
            if die > 100:
                die -= 100

        p1_loc = (p1_move + p1_loc) %10
        if p1_loc == 0: p1_score+=10
        else: p1_score += p1_loc

        if p1_score >= 1000:
            break

        #p2 move
        p2_move = 0
        for i in range(3):
            die_roll += 1
            p2_move +=die
            die+=1
            if die > 100:
                die -= 100

        p2_loc = (p2_move + p2_loc) %10
        if p2_loc == 0: p2_score+=10
        else: p2_score += p2_loc

        if p2_score >= 1000:
            break

    loser_score = min(p2_score, p1_score)
    print('roll',die_roll)
    print('loser score',loser_score)
    print('answ', die_roll*loser_score)


'''
3 (1 1 1) -> 1
4 (1 1 2) -> 123
5 (1 2 2, 3 1 1) -> 123456
6 (1 2 3, 2 2 2) -> 1234567
7 (2 2 3, 3 3 1) -> 123456
8 (3 3 2) -> 123
9 (3 3 3) -> 1
'''

# Index is the 3 die rolls added together.
# Value is number of times you'll hit that value in the 27 possibilities
outcomes = [0,0,0,1,3,6,7,6,3,1]
print('outcomes:', sum(outcomes))


END_POINTS = 21
SPOTS = 10
# p1pts,p2pts,p1loc,p2loc
def clear_matrix():
    master = []
    for p1pt in range(END_POINTS):
        master.append([])
        for p2pt in range(END_POINTS):
            master[p1pt].append([])
            for p1loc in range(SPOTS):
                master[p1pt][p2pt].append([])
                for p2loc in range(SPOTS):
                    master[p1pt][p2pt][p1loc].append(0)
    return(master)

import copy 
dcopy = copy.deepcopy


# p1pts,p2pts,p1loc,p2loc
master = clear_matrix()
master[0][0][7][5] +=1 # initial game
master_out = clear_matrix()

'''
for p1pt in range(END_POINTS):
    for p2pt in range(END_POINTS):
        for p1loc in range(SPOTS):
            for p2loc in range(SPOTS):
                if master[p1pt][p2pt][p1loc][p2loc] != 0:
                    print('p1 pt, loc:', p1pt, p1loc)
                    print('p2 pt, loc:', p2pt, p2loc)
                    print(master[p1pt][p2pt][p1loc][p2loc]) 
                if master_out[p1pt][p2pt][p1loc][p2loc] != 0:
                    print('p1 pt, loc:', p1pt, p1loc)
                    print('p2 pt, loc:', p2pt, p2loc)
                    print(master_out[p1pt][p2pt][p1loc][p2loc]) 
                    '''
    

p1_winners = 0
p2_winners = 0
loop=0
while True:
    print('loop:',loop)
    empty_count = 0
    for p1pt in range(END_POINTS):
        for p2pt in range(END_POINTS):
            for p1loc in range(SPOTS):
                for p2loc in range(SPOTS):
                    if master[p1pt][p2pt][p1loc][p2loc] == 0:
                        empty_count +=1
                        continue
                    num_here = master[p1pt][p2pt][p1loc][p2loc] 
                    #master_out[p1pt][p2pt][p1loc][p2loc] = 0 # This methodology was my bug.
                    for outcome, count in enumerate(outcomes):
                        if count == 0:
                            continue
                        cur_p1_loc = (p1loc + outcome) % 10
                        if cur_p1_loc == 0:
                            cur_p1_pts = 10 + p1pt
                        else:
                            cur_p1_pts = cur_p1_loc + p1pt
                        if cur_p1_pts >= END_POINTS:
                            p1_winners += num_here * count
                        else:
                            # This found my bug:
                            #if master_out[cur_p1_pts][p2pt][cur_p1_loc][p2loc] !=0:
                            #    print("WARNING")
                            master_out[cur_p1_pts][p2pt][cur_p1_loc][p2loc] += num_here*count

    master = dcopy(master_out)
    master_out = clear_matrix() # Second part of the bug fix.
    
    if empty_count >= (END_POINTS)*(END_POINTS)*SPOTS*SPOTS:
        break
    
    '''
    num_points = 0
    num_points_out = 0
    for p1pt in range(END_POINTS):
        for p2pt in range(END_POINTS):
            for p1loc in range(SPOTS):
                for p2loc in range(SPOTS):
                    if master[p1pt][p2pt][p1loc][p2loc] != 0:
                        num_points += master[p1pt][p2pt][p1loc][p2loc]
                        #print('p1 pt, loc:', p1pt, p1loc)
                        #print('p2 pt, loc:', p2pt, p2loc)
                        #print(master[p1pt][p2pt][p1loc][p2loc]) 
    '''
    
    
    empty_count = 0
    for p1pt in range(END_POINTS):
        for p2pt in range(END_POINTS):
            for p1loc in range(SPOTS):
                for p2loc in range(SPOTS):
                    if master[p1pt][p2pt][p1loc][p2loc] == 0:
                        empty_count +=1
                        continue
                    num_here = master[p1pt][p2pt][p1loc][p2loc] 
                    #master_out[p1pt][p2pt][p1loc][p2loc] = 0 # Bug
                    for outcome, count in enumerate(outcomes):
                        if count == 0:
                            continue
                        cur_p2_loc = (p2loc + outcome) % 10
                        if cur_p2_loc == 0:
                            cur_p2_pts = 10 + p2pt
                        else:
                            cur_p2_pts = cur_p2_loc + p2pt
                        if cur_p2_pts >= END_POINTS:
                            p2_winners += num_here * count
                        else:
                            master_out[p1pt][cur_p2_pts][p1loc][cur_p2_loc] += num_here*count

    master = dcopy(master_out)
    master_out = clear_matrix() # bug fix

    if empty_count >= (END_POINTS)*(END_POINTS)*SPOTS*SPOTS:
        break
    loop+=1

print('p1_winners', p1_winners)
print('p2_winners', p2_winners)


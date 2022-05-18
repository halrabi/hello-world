"""This program computes the score for a bridge contract hand.
     The user inputs:
       the level and strain of the contract,
       the number of tricks made above contract, or
       the number of tricks short,
       the vulnerability,
       and whether the contract was undoubled, doubled, or redoubled.
    Then the program concisely describes the contract and the outcome
    and reports the score from a precomputed table."""

# Updated 05/10/2022

import sys

def bl_score(level, strain, made, down):
    """Compute Below the Line Score."""
    temp_bl = [0, 0, 0, 0, 0, 0]
    if down == 0:
        if strain == 'C' or strain == 'D':
            temp_bl[0] = int(level) * 20
            temp_bl[3] = temp_bl[0]
            temp_bl[1] = temp_bl[0] * 2
            temp_bl[4] = temp_bl[1]
            temp_bl[2] = temp_bl[1] * 2
            temp_bl[5] = temp_bl[2]

        elif strain == 'H' or strain =='S':
            temp_bl[0] = int(level) * 30
            temp_bl[3] = temp_bl[0]
            temp_bl[1] = temp_bl[0] * 2
            temp_bl[4] = temp_bl[1]
            temp_bl[2] = temp_bl[1] * 2
            temp_bl[5] = temp_bl[2]

        elif strain == ('NT'):
            temp_bl[0] = 40 + (int(level) -1) * 30
            temp_bl[3] = temp_bl[0]
            temp_bl[1] = temp_bl[0] * 2
            temp_bl[4] = temp_bl[1]
            temp_bl[2] = temp_bl[1] * 2
            temp_bl[5] = temp_bl[2]

        else:
            print(f"The strain {strain} is not valid>")
            sys.exit()
       
    return temp_bl

def ot_score(level, strain, made, down):
    """Compute Overtrick Score."""
    temp_ot = [0, 0, 0, 0, 0, 0]
    if down == 0:
        if strain == 'C' or strain == 'D':
            temp_ot[0] = (int(made) - int(level)) * 20
            temp_ot[3] = temp_ot[0]
            temp_ot[1] = (int(made) - int(level)) * 100
            temp_ot[4] = (int(made) - int(level)) * 200
            temp_ot[2] = (int(made) - int(level)) * 200
            temp_ot[5] = (int(made) - int(level)) * 400
        
        elif strain == 'H' or strain == 'S':
            temp_ot[0] = (int(made) - int(level)) * 30 
            temp_ot[3] = temp_ot[0]
            temp_ot[1] = (int(made) - int(level)) * 100
            temp_ot[4] = (int(made) - int(level)) * 200
            temp_ot[2] = (int(made) - int(level)) * 200
            temp_ot[5] = (int(made) - int(level)) * 400

        elif strain == 'NT':
            temp_ot[0] = (int(made) - int(level)) * 30 
            temp_ot[3] = temp_ot[0]
            temp_ot[1] = (int(made) - int(level)) * 100
            temp_ot[4] = (int(made) - int(level)) * 200
            temp_ot[2] = (int(made) - int(level)) * 200
            temp_ot[5] = (int(made) - int(level)) * 400
            
    return temp_ot

def ps_bonus(below_line_score):
    """Compute Part Score Bonus."""
    temp_ps = [0, 0, 0, 0, 0, 0]
    for i in range(0,6):
        if below_line_score[i] < 100 and below_line_score[i] > 0:
            temp_ps[i] = 50

    return temp_ps

def g_bonus(below_line_score):
    """Compute Game Bonus."""
    temp_gb = [0, 0, 0, 0, 0, 0]
    for i in range(0,6):
        if below_line_score[i] >= 100:
            if i <= 2:
                temp_gb[i] = 300
            else:
                temp_gb[i] = 500

    return temp_gb

def sl_bonus(level, down):
    """Compute Slam Bonus."""
    temp_sb = [0, 0, 0, 0, 0, 0]
    if down == 0:
        if level == '6':
            temp_sb = [500, 500, 500, 750, 750, 750]
        if level == '7':
            temp_sb = [1000, 1000, 1000, 1500, 1500, 1500]
    return temp_sb

def i_bonus(down):
    """Compute Insult Bonus."""
    temp_ib = [0, 0, 0, 0, 0, 0]
    if down == 0:
        temp_ib = [0, 50, 100, 0, 50, 100]
    return temp_ib

def dn_score(level, down):
    """Compute Penalty for Going Down."""
    temp_dn = [0, 0, 0, 0, 0, 0]
    down = int(down)
    level = int(level)
    if down == 0:
        temp_dn = temp_dn
    elif down == 1:
        temp_dn = [50, 100, 200, 100, 200, 400]
    elif down == 2:
        temp_dn = [100, 300, 600, 200, 500, 1000]
    elif down == 3:
        temp_dn = [150, 500, 1000, 300, 800, 1600]
    elif down > 3 and down <= (level + 6):
        temp_dn[0] = 150 + (down - 3) * 50 
        temp_dn[1] = 500 + (down - 3) * 300
        temp_dn[2] = 1000 + (down - 3) * 600
        temp_dn[3] = 300 + (down - 3) * 100
        temp_dn[4] = 800 + (down - 3) * 300
        temp_dn[5] = 1600 + (down - 3) * 600
    else:
        print("down out of range")
        sys.exit()
        
    return temp_dn


q = False
while q == False:
    made = 0
    down = 0
    # Receive description of contract from user
    print("Welcome to the Contract Bridge Scoring Program")
    print("Please answer the following questions:")
    level = input("Contract Level? (1 to 7): ")
    klevel = int(level)
    if (klevel < 1) or (klevel > 7):
        print(f"Contract level {level} is out of range.")
        sys.exit()
    strain = input("Contract Strain? (C, D, H, S, or NT): ")
    strain = f"{strain.upper()}"
    contract = level + strain

    # Did you make the contract or go down?
    make = input("Did you make the contract? (Y or N): ")
    make = f"{make.upper()}"
    if make != 'Y':
        if make != 'N':
            print("Failed to answer Y or N.")
            sys.exit()

    vul = input(f"Were you vulnerable? (Y or N): ")
    vul = f"{vul.upper()}"
    if vul != 'Y':
        if vul != 'N':
            print("Failed to answer Y or N.")
            sys.exit()

    dbl = input(f"Was the contract Undoubled, Doubled, or Redoubled? (U, D, or R): ")
    dbl = f"{dbl.upper()}"


    # How many did you make or go down?

    if make == 'Y':
        # How many did you make?
        made = input("How many did you make? (number between level and 7): ")
        lmade = int(made)
        if lmade < klevel or lmade > 7:
            print("Made is out of range")
            sys.exit()
        else:
            print(f"Your Contract is {contract}, vul = {vul}, dbl = {dbl}, Made {made}")
    
    else:
        # How many were you down?
        down = input("How many did you go down?:(number between 1 and (bid level + 6): ")
        print(f"Your Contract is {contract}, vul = {vul}, dbl = {dbl}, Down {down}")
    if vul  == 'N':
        if dbl == 'U':
            col = 0
        if dbl == 'D':
            col = 1
        if dbl == 'R':
            col = 2

    elif vul == 'Y':
        if dbl == 'U':
            col = 3
        if dbl == 'D':
            col = 4
        if dbl == 'R':
            col = 5
    total_score = [0, 0, 0, 0, 0, 0]    
    below_line_score = bl_score(level, strain, made, down)
    overtrick_score = ot_score(level, strain, made, down)
    part_score_bonus = ps_bonus(below_line_score)
    game_bonus_score = g_bonus(below_line_score)
    slam_bonus_score = sl_bonus(level, down)
    insult_bonus_score = i_bonus(down)
    down_score = dn_score(level, down)
    y = str(below_line_score[col])
    spcs = len(y)
    print(f"Below Line Score:{(' ') * (6 - spcs)} {below_line_score[col]}")
    y = str(overtrick_score[col])
    spcs = len(y)
    print(f"Overtrick Score: {(' ') * (6 - spcs)} {overtrick_score[col]}")
    y = str(part_score_bonus[col])
    spcs = len(y)
    print(f"Part Score Bonus:{(' ') * (6 - spcs)} {part_score_bonus[col]}")
    y = str(game_bonus_score[col])
    spcs = len(y)
    print(f"Game Bonus:      {(' ') * (6 - spcs)} {game_bonus_score[col]}")
    y = str(slam_bonus_score[col])
    spcs = len(y)
    print(f"Slam Bonus:      {(' ') * (6 - spcs)} {slam_bonus_score[col]}")
    y = str(insult_bonus_score[col])
    spcs = len(y)
    print(f"Insult Bonus:    {(' ') * (6 - spcs)} {insult_bonus_score[col]}")
    y = str(down_score[col])
    spcs = len(y)
    print(f"Penalty (Down): {(' ') * (6 - spcs)}  {down_score[col]}")
    total_score[col] = below_line_score[col] + overtrick_score[col] + part_score_bonus[col]
    total_score[col] += game_bonus_score[col] + slam_bonus_score[col] + insult_bonus_score[col]
    total_score[col] -= down_score[col]
    y = str(total_score[col])
    spcs = len(y)
    print(f"Total Score:     {(' ') * (6 - spcs)} {total_score[col]}")
    
    getout = input(f"Would you like to score another hand? (Y or N): ")
    getout = f"{getout.upper()}"
    if getout == 'Y':
        q = False
    else:
        q = True
    

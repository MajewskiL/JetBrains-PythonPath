import random
change_who = {"X": "O", "O": "X"}


def oko():  # Show battlefield
    print("   1 2 3")
    print(" ---------")
    for x in range(3):
        print(f"{3 - x}| {battle_field[3 * x] if battle_field[3 * x] != '_' else ' '}"
              f" {battle_field[3 * x + 1] if battle_field[3 * x + 1] != '_' else ' '}"
              f" {battle_field[3 * x + 2] if battle_field[3 * x + 2] != '_' else ' '} |")
    print(" ---------")


def count_sign():  # Count numbers of XO
    strb = "".join(battle_field)
    return [strb.count("X"), strb.count("O")]


def check_field(battle_f, who):
    line = []
    for x in range(3):
        line.append(all([z == who for z in battle_f[3 * x: 3 * x + 3]]))
        line.append(all([battle_f[z] == who for z in (x, x + 3, x + 6)]))
    line.append(all([battle_f[x] == who for x in (0, 4, 8)]))
    line.append(all([battle_f[x] == who for x in (2, 4, 6)]))
    return any(line)


def check_third(who):
    for x in range(3):
        txt = "".join([z for z in battle_field[3 * x: 3 * x + 3]])
        if txt.count(who) == 2 and txt.count(change_who[who]) == 0:
            return 3 * x + txt.index("_") + 1
        txt = "".join([battle_field[z] for z in (x, x + 3, x + 6)])
        if txt.count(who) == 2 and txt.count(change_who[who]) == 0:
            return x + txt.index("_") * 3 + 1
    txt = "".join([battle_field[x] for x in (0, 4, 8)])
    if txt.count(who) == 2 and txt.count(change_who[who]) == 0:
        return txt.index("_") * 4 + 1
    txt = "".join([battle_field[x] for x in (2, 4, 6)])
    if txt.count(who) == 2 and txt.count(change_who[who]) == 0:
        return (txt.index("_") + 1) * 2 + 1
    return False


def check_numbers(coordinates):
    if len(coordinates) != 2 or not all([coordinates[0].isdigit(), coordinates[1].isdigit()]):
        print("You should enter numbers!")
        return False
    coordinates = [int(x) for x in coordinates]
    if any([coordinates[x] not in [1, 2, 3] for x in range(2)]):
        print("Coordinates should be from 1 to 3!")
        return False
    return (3 - coordinates[1])*3 + coordinates[0]


def go_robot(who, level):
    """ HARD """
    if level == "hard":
        return terminator(battle_field, who, who)[1] + 1
    """ MEDIUM """
    if level == "medium":
        for x in [who, change_who[who]]:
            xy = check_third(x)
            if xy:
                return xy
    """ EASY """
    bag = [x for x in range(9) if battle_field[x] == "_"]
    random.shuffle(bag)
    return bag[0] + 1


def battle(ai_iq):
    qt, who, cnt = True, "X", 0
    while qt:
        if ai_iq[cnt % 2] == "user":
            coordinates = [x for x in input(f"{who} Enter the cooridnates: ").split(" ")]
            xy = check_numbers(coordinates)
        else:
            print(f'{who} Making move level "{ai_iq[cnt % 2]}"')
            xy = go_robot(who, ai_iq[cnt % 2])
        if xy:
            xy -= 1
            cnt += 1
            if battle_field[xy] == "_":
                battle_field[xy] = who
                oko()
                counts = count_sign()
                if check_field(battle_field, who):
                    print(f"{who} wins")
                    qt = False
                elif sum(counts[:]) == 9:
                    print("Draw")
                    qt = False
                who = change_who[who]
            else:
                print("This cell is occupied! Choose another one!")
                cnt -= 1


def terminator(board, who, turn):
    scores = {x: -10 for x in range(9) if board[x] not in "XO"}
    if board.count("_") == 0:
        return 0
    if check_field(board, change_who[who]):
        return -10 if turn == who else 10
    for x in scores.keys():
        board_tmp = board.copy()
        board_tmp[x] = who
        wyn = terminator(board_tmp, change_who[who], turn)
        scores[x] = wyn if wyn in (-10, 0, 10) else wyn[0]
    if who == turn:
        return [scores[max(scores, key=scores.get)], max(scores, key=scores.get)]
    return [scores[min(scores, key=scores.get)], min(scores, key=scores.get)]


while True:
    tryb = input("Input command:").split(" ")
    if tryb[0] == "exit":
        break
    if all([tryb[0] == "start", len(tryb) == 3,
            all([tryb[x] in ["easy", "medium", "hard", "user"] for x in range(1, len(tryb))])]):
        battle_field = ["_"]*9
        oko()
        battle({0: tryb[1], 1: tryb[2]})
    else:
        print("Bad parameters!")

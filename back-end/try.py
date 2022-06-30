from game import Connect_4

a = Connect_4("xd", True)

while True:
    board = [[] for _ in range(6)]
    for column in a.board:
        for y, square in enumerate(column):
            board[y].append(square)

    for row in board:
        print(row)
    loc = input("Enter coordinate e.g. col,row: ").split(",")
    finished = a.make_move((int(loc[0]),int(loc[1])))
    if finished:
        print("Winner:", a.current_player)
        break
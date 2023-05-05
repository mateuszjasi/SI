import connect_ai as cai
import connect_puzzle as cp
import time

SEARCH_DEPTH = 100
connect = cp.Connect()
while connect.has_winner() == 0:
    connect.print_turn()
    t = time.time()
    connect.play_move(cai.choose_move(connect, SEARCH_DEPTH))
    t = (time.time() - t) * 1000
    connect.print_board()
    print(t)

    connect.print_turn()
    human_move_result = False
    while human_move_result is False:
        print('Make your move: ')
        human_move = int(input())
        human_move_result = connect.play_move(human_move)
    connect.print_board()

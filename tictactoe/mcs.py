import random
def random_action(board,is_my_action):
  legal_moves = board.legal_moves()
  board = board.place_piece(random.choice(legal_moves),is_my_action)
  current_status = board.is_win_or_lose()
  if current_status == "win":
    return 1
  if current_status == "lose":
    return -1
  if current_status == "draw":
    return 0
  return random_action(board,not is_my_action)


def mcs_main(board):
  score = {}
  for e in board.legal_moves():
    score[e] = 0
    for p in range(100):
      score[e] += random_action(board,True)
  return max(score,key = score.get)
import random



class State:
  def __init__(self,pieces= None,enemy_pieces=None):
    self.pieces = pieces if pieces != None else [0] * 9
    self.enemy_pieces = enemy_pieces if enemy_pieces != \
    None else [0] * 9

  def piece_count(self,pieces):
    count = 0
    for i in pieces:
      if i == 1:
        count += 1
    return count

  def is_win(self, pieces):
    def is_comp(x,y,dx,dy):
      for k in range(3):
        if y < 0 or 2 < y or x < 0 or 2 < x or \
          pieces[x+y*3] == 0:
          return False
        x , y = x+dx , x+dy
      return True
    if is_comp(0,0,1,1) or is_comp(0,2,1,-1):
      return True
    for i in range(3):
      if is_comp(0,i,1,0) or is_comp(i,0,0,1):
        return True
    return False  

  def is_draw(self):
    return self.piece_count(self.pieces) + self.piece_count\
      (self.enemy_pieces) == 9

  def is_done(self):
    return self.is_win(self.enemy_pieces) or self.is_draw() or self.is_win(self.pieces)

  def next(self,action,is_my_action):
    if is_my_action:
      pieces = self.pieces.copy()
      pieces[action] = 1
      return State(pieces, self.enemy_pieces)
    else:
      enemy_pieces = self.enemy_pieces.copy()
      enemy_pieces[action] = 1
      return State(self.pieces, enemy_pieces)


  def legal_actions(self):
    actions = []
    for i in range(9):
      if self.pieces[i] == 0 and self.enemy_pieces[i] == 0:
        actions.append(i)
    return actions

  def is_first_player(self):
    return self.piece_count(self.pieces) == self.piece_count(self.enemy_pieces)

  def __str__(self):
    ox = ('o','x')
    output = ''

    for i in range(9):
      if self.pieces[i] == 1:
        output += ox[0]
      elif self.enemy_pieces[i] == 1:
        output += ox[1]
      else:
        output += '-'
      if i % 3 == 2:
        output += '\n'
    return output

  #################### Minimax functions ########################## 
  def place_piece(self,action,is_my_action):
    return self.next(action,is_my_action)
  def legal_moves(self):
    return self.legal_actions()
  def is_win_or_lose(self):
    if self.is_done():
      if self.is_win(self.enemy_pieces):
        return 'lose'
      elif self.is_win(self.pieces):
        return 'win'
      elif self.is_draw():
        return 'draw'
    return 'not finished'
def player_vs_computer(board,tactic_book):
  while board.is_win_or_lose() == "not finished":
    smart_moves = tactic_book.get_children_by_value()
    children_pos = random.randint(0, len(smart_moves)-1)
    board = board.place_piece(smart_moves[children_pos].move,True)
    tactic_book = smart_moves[children_pos]
    print(board)
    human_move = int(input())
    board = board.place_piece(human_move,False)
    tactic_book = tactic_book.get_child_by_move(human_move)
    print(board)
    print(board.is_win_or_lose())
if __name__ == "__main__":
  import mini_max
  board = State()
  test_board = State([1, 0, 0, 1, 0, 0, 0, 1, 0],[0, 0, 0, 0, 1, 0, 1, 0, 1])
  print(test_board.is_win_or_lose())
  tactic_book = mini_max.Mini_max(board).tree
  player_vs_computer(board,tactic_book)  

  
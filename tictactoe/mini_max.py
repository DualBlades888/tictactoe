import sys
import copy
class Tree:
  def __init__(self, value,move):
    self.value = value
    self.children = []
    self.move = move
  def get_children_by_value(self):
    result = []
    for e in self.children:
      if self.value == e.value:
        result.append(e)
    return result
  def add_child(self, obj):
    self.children.append(obj)
  def get_child_by_move(self,move):
    for e in self.children:
      if e.move == move:
        return e
class Mini_max:
  def __init__(self,board):
    self.tree = self.best_solution(board)
    
  def best_solution(self, board, depth=0, current_move=None, alpha=-sys.maxsize, beta=sys.maxsize): ## output tree obj
    # board obj contain (is_win_or_lose function ,legal_moves function , place_piece function)
    current_status = board.is_win_or_lose()
    result = Tree(0,current_move)
    is_my_action = True

    if depth %2 == 0:
      is_my_action = True
    else:
      is_my_action = False

    if current_status == "win":
      result.value =  1
    elif current_status == "lose":
      result.value = -1
    elif current_status == "draw":
      result.value = 0
    else:
      for e in board.legal_moves():
        sub_board = board.place_piece(e,is_my_action)
        child_member = self.best_solution(sub_board,depth+1,e)
        # child_member.value = 0
        result.add_child(child_member)
      if depth % 2 == 0:
        result.value = max(result.children, key=lambda item: item.value).value
      if depth % 2 == 1:
        result.value = min(result.children, key=lambda item: item.value).value
    return result 
     

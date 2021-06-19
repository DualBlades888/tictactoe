import random
import math
from sys import path
class Node:
  def __init__(self, wins,attempts,move,parent):
    self.wins = wins
    self.parent = parent
    self.children = []
    self.attempts = attempts
    self.move = move
class Mcs_tree:
  def __init__(self,board):
    self.initialize(board)
  def random_action(self,board,is_my_action):
    legal_moves = board.legal_moves()
    current_status = board.is_win_or_lose()
    if current_status == "win":
      return 1
    if current_status == "lose":
      return -1
    if current_status == "draw":
      return 0
    board = board.place_piece(random.choice(legal_moves),is_my_action)
    return self.random_action(board,not is_my_action)

  def find_biggest_UCB(self,root):
    #e.wins/e.attempts + math.sqrt(2*math.log(self.total_attempts)/e.attempts)
    max_node = root
    if root == self.decision_node:
      max_node = root.children[0]
    if root.children == []:
      return root
    for e in root.children:
      children_best = self.find_biggest_UCB(e)
      if children_best.attempts == 0:
        return children_best
      if self.UCB1(children_best)>self.UCB1(max_node):
        max_node = children_best
    return max_node
  def find_biggest_attempts(self,root):
    max_node = root
    if root == self.decision_node:
      max_node = root.children[0]
    if root.children == []:
      return root
    for e in root.children:
      if e.attempts > max_node.attempts:
        max_node = e
    return max_node
  def UCB1(self,node):
    return node.wins/node.attempts + math.sqrt(2*math.log(self.total_attempts)/node.attempts)
  
  def find_path(self,node,path=[]): # node path doesn't include decision node(include node) return node.move
    if node == self.decision_node:
      return path[::-1]
    path.append(node.move)
    return self.find_path(node.parent,path)
  def get_all_parent_node(self,node,parents=[]):#parents  include decision node(include node) return node obj 
    if node == self.decision_node:
      parents.append(self.decision_node)
      return parents
    parents.append(node)
    return self.get_all_parent_node(node.parent,parents)
  def play_board_to_node_move(self,path,board):
    is_my_action = True
    simulate_board = board
    for e in path:
      simulate_board = simulate_board.place_piece(e,is_my_action)
      is_my_action = not is_my_action
    return simulate_board, is_my_action
  def initialize(self,board):
    #######settings#####
    self.expansion_max_number = 10
    self.playout_times = 100
    ##########################
    ###### create tree #####
    self.total_attempts = 0
    
    self.decision_node= Node(0,0,None,None)
    for e in board.legal_moves():
      self.decision_node.children.append(Node(0,0,e,self.decision_node))
  def mcs_main(self,board):
    self.initialize(board)
    for e in range(self.playout_times):
      ###########decide###########
      find_node = self.find_biggest_UCB(self.decision_node)
      path = self.find_path(find_node)
      ###########################
      #########playout############
      current_board,is_my_action = self.play_board_to_node_move(path,board)
      score = self.random_action(current_board,is_my_action)

      ############################
      ########expand#########
      if find_node.attempts >= 10:
        legal_moves = current_board.legal_moves()
        for e in legal_moves:
          find_node.children.append(Node(0,0,e,find_node))
      ########################
      ##########update#######
      for e in self.get_all_parent_node(find_node):
        e.wins += score
        e.attempts += 1
      self.total_attempts += 1
      ####################
    return self.find_biggest_attempts(self.decision_node).move
      
      
      


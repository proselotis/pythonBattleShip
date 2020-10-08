"""Main """

import os 
import sys 

# Board = 1 
# shot_request = 2
# shot_result = 3
# end_game = 0
READ_SIZE = sys.getsizeof("0")

BOARD_ROWS = 8
BOARD_COLS = 8
template_board = str([
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,33,33,33,0],
         [0,0,44,0,0,0,0,22],
         [0,0,44,0,0,55,0,22],
         [0,0,44,0,0,55,0,22],
         [0,0,44,0,0,55,0,0],
         [0,0,0,0,0,55,0,11],
         [0,0,0,0,0,55,0,11]
   ])


class Player():
   def __init__(self,in_pipe,output):
      self.in_pipe = in_pipe
      self.output = output

def close_pipes(*pipes):
   for pipe in pipes:
      os.close(pipe)

def readBoard(player):
   read_list = [int(i.replace("]","").replace("[","")) for i in os.read(player.in_pipe,sys.getsizeof(template_board)).decode().strip('][').split(", ")]
   return [read_list[i:i + BOARD_ROWS] for i in range(0,len(read_list),BOARD_ROWS)]

def getShot(player):
   os.write(player.output,"2".encode())
   return os.read(player.in_pipe,sys.getsizeof("[0,0]")).decode()

def sendShot(player,shot):
   # import time
   # os.write(player.output,"3".encode())
   # time.sleep(1)
   # os.write(player.output,shot.encode())
   pass
def sendResult(player,opponent_board,shot):
   a = int(shot[1])
   b = int(shot[4])
   if int(opponent_board[a][b]) < 0:
      os.write(player.output,"mis".encode())
   else:
      os.write(player.output,"hit".encode())
   opponent_board[a][b] = -1
   return opponent_board

def winCheckHelper(board):
   win = True
   for i in range(BOARD_ROWS):
      for j in range(BOARD_COLS):
         if board[i][j] > 0:
            return False
   return True
def winCheck(board_1,board_2):
   p1_result = winCheckHelper(board_1)
   p2_result = winCheckHelper(board_2)
   if p1_result and p2_result:
      return 3
   elif p1_result:
      return 1
   elif p2_result:
      return -1
   else:
      return 0
def playGame(p1,p2):
   # Ask for boards
   os.write(p1.output,"1".encode())
   os.write(p2.output,"1".encode())

   # Read boards
   p1_board = readBoard(p1)
   p2_board = readBoard(p2)
   # loop through shots 
   rounds = 0
   while True:
      print(rounds)
      rounds += 1 
      shot = getShot(p1)
      sendShot(p2,shot)
      p2_board = sendResult(p1,p2_board,shot)

      shot = getShot(p2)
      sendShot(p1,shot)
      p1_board = sendResult(p2,p1_board,shot)

      res = winCheck(p1_board,p2_board)
      if res != 0: 
         return res 



def playGames(games, p1,p2):
   game = 0
   while games != game:
      result = playGame(p1,p2)
      print(result)
      game += 1 


# Make pipes for all the players 
in_a, out_a = os.pipe()
in_b, out_b = os.pipe()
in_c, out_c = os.pipe()
in_d, out_d = os.pipe()

os.set_inheritable(in_b,True)
os.set_inheritable(in_c,True)

os.set_inheritable(out_a,True)
os.set_inheritable(out_d,True)




pid_1 = os.fork()
if pid_1 == 0: 
   close_pipes(in_a,in_b,in_d,out_a,out_b,out_c)
   os.system("python3 basicPlayer.py {} {}".format(str(in_c),str(out_d)))
   close_pipes(in_c,out_d)
   print("player 2 end")

elif pid_1 != 0:
   pid_2 = os.fork()
   if pid_2 == 0:
      # start player 1
      close_pipes(in_a,in_c,in_d,out_b,out_c,out_d)
      os.system("python3 basicPlayer.py {} {}  ".format(str(in_b),str(out_a)))
      close_pipes(in_b,out_a)
      print("player 1 end")
   else:
      close_pipes(in_b,in_c,out_a,out_d) 
      playGames(1,Player(in_a,out_b),Player(in_d,out_c))
      os.waitpid(-1, os.WNOHANG)




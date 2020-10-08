import sys 
import os 

BOARD_ROWS = 8
BOARD_COLS = 8

READ_SIZE = sys.getsizeof("0")

read_from = int(sys.argv[1])
 # = os.fdopen(t1,"r")

write_to = int(sys.argv[2])
 # = os.fdopen(t2,"w")

   
def makeBoard():
   return str([
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,33,33,33,0],
         [0,0,44,0,0,0,0,22],
         [0,0,44,0,0,55,0,22],
         [0,0,44,0,0,55,0,22],
         [0,0,44,0,0,55,0,0],
         [0,0,0,0,0,55,0,11],
         [0,0,0,0,0,55,0,11]
   ])
def getShot(row,col):
   if col == 8:
      raise Exception("sendShot function is busted")
   elif row == 8:
      row = 0 
      col +=1 
   shot = [row,col]
   row += 1 
   return [shot,row,col]
def readShot(read_pipe):
   return os.read(read_pipe,sys.getsizeof("[0,0]"))
def readResult(read_pipe):
   return os.read(read_pipe,sys.getsizeof("hit"))


row = col = 0
while True:
   request = os.read(read_from,READ_SIZE).decode()
   # print("request: ",request)
   if request == "1":
      os.write(write_to,makeBoard().encode())
   elif request == "2":
      shot,row,col = getShot(row,col)
      os.write(write_to,str(shot).encode())
      readResult(read_from)
   elif request == "3":
      opponentShot = readShot(read_from)
   elif request == "0":
      break
print("player end")
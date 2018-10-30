######### File manipulation ###############
f =open("map.txt","r")
Data = f.readlines()
Data = [x.strip('\n') for x in Data]
f.close()

########### Get meta info ################
info= Data[0].split(" ")
width = int(info[0])
height = info[1]
NumDiamonds = info[2]

Data.pop(0) # pop meta info out.

###########  Print Map ###################
for x in range(len(Data)):
    print Data[x]

###############   Mapping    ######################################
# M = robot start      J = Diamond     G = goal/dimond destination
# . = Road             X = wall        " " = no map
isRoad='.'
RoadAdjencyList = [[]for i in range(len(Data)) ]
isDiamond = 'J'
Diamonds = []
isGoal = 'G'
Goals = []
isRobotStart = 'M'
isWall = 'X'
RobotStart = []
list = []

# Check if walkaable field or X, save Road, Diammond etc.
for i in range(len(Data)):
    for j in range(len(Data[i])):
        if  Data[i][j] == isRoad:
            RoadAdjencyList[i].append(j)
    #        list.append(j)
        elif Data[i][j] == isDiamond:
            Diamonds.append([i,j])
            RoadAdjencyList[i].append(j)
        elif Data[i][j] == isGoal:
            Goals.append([i,j])
            RoadAdjencyList[i].append(j)
        elif Data[i][j] == isRobotStart:
            RobotStart.append(i)
            RobotStart.append(j)
            RoadAdjencyList[i].append(j)
    #if len(list)!= 0 :
    #    RoadAdjencyList[i].append(list)
    #list = []


########## Print lists ############################
print("\nAdjencylis:\n")
print(RoadAdjencyList)

print("\nDiamonds:\n")
print(Diamonds)

print("\nGoals:\n")
print(Goals)

print("\nRobotStart:\n")
print(RobotStart)

print("______________________________")

############# Game as a class ####################
class State(object):
    Road = []
    Diamonds = []
    Goals = []
    Player = []
    width=0
    # The class "constructor" - It's actually an initializer
    def __init__(self, Road, Diamonds, Goals, Player, width):
        self.Road = Road
        self.Diamonds = Diamonds
        self.Goals = Goals
        self.Player = Player
        self.width= width

    def PMap (self):
        line = ""
        R = 0 # Road
        supR = 0 # Sup Road
        D = 0 #Diamond counter
        G = 0 # Goals
        P = 0 # Robot player
        nextChar = ''

        for i in range(len(self.Road)):
            for j in range(self.width):

                if len(self.Road[R])>0:
                    if self.Road[R][supR] == j and R == i:
                        nextChar='.'
                        if supR < len(self.Road[R])-1:
                            supR+=1

                if self.Goals[G] == [i,j]:   # Need to handle when goal is under player/
                    nextChar='G'
                    if G < len(Goals)-1:
                        G+=1

                if [i,j] in self.Diamonds: # needs to check all dimonds, can be moved.
                    nextChar='J'
                    #print self.Diamonds[D] , [i,j]
                    if D < len(self.Diamonds)-1:
                        D+=1

                if self.Player[0] == i and self.Player[1] == j:
                    nextChar='M'

                if nextChar=='':
                    nextChar='X'

                line+=nextChar
                nextChar =''
            print(line)
            line = ""
            L = 0
            R+=1
            supR=0
            #print R
        return;

    def up (self):
        row = self.Player[0]-1
        col = self.Player[1]
        DoubleDimond = False
        DimondBlocked=False
        if [row,col] in self.Diamonds:
            # move Diamond
            if [row-1,col] in self.Diamonds:
                DoubleDimond=True
            else:#no dimond besides dimond
                for i in range(len(Diamonds)): #Find dimond and check if its movable
                    if [row,col] == Diamonds[i]:
                        for j in range(len(Diamonds)):
                            if [row-1,col] == Diamonds[j]:
                                DimondBlocked=True
                        if col in self.Road[row-1]: #Road pice after moved.... NO EXCEPTIon CATCH
                            if not DimondBlocked: # check for not blocked
                                Diamonds[i]=[row-1,col]
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond:
            self.Player[0]=row

        if self.Player[0] == row:
            return True;
        else:
            return False;
    def down (self):
        row = self.Player[0]+1
        col = self.Player[1]
        DoubleDimond=False
        DimondBlocked=False

        if [row,col] in self.Diamonds:
            if [row+1,col] in self.Diamonds:
                DoubleDimond=True
            else:#no dimond besides dimond
                for i in range(len(Diamonds)): #Find dimond and check if its movable
                    if [row,col] == Diamonds[i]:
                        for j in range(len(Diamonds)):
                            if [row+1,col] == Diamonds[j]:
                                DimondBlocked=True
                        if col in self.Road[row+1]: #Road pice after moved.... NO EXCEPTIon CATCH
                            if not DimondBlocked: # check for not blocked
                                Diamonds[i]=[row+1,col]
                        else: #There is a isWall
                            DimondBlocked = True


        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            self.Player[0]=row

        if self.Player[0] == row:
            return True;
        else:
            return False;
    def right (self):
        row = self.Player[0]
        col = self.Player[1]+1
        DoubleDimond=False
        DimondBlocked=False

        if [row,col] in self.Diamonds:
            if [row,col+1] in self.Diamonds: #Dimond next to diamond
                DoubleDimond=True
            else:#no dimond besides dimond
                for i in range(len(Diamonds)): #Find dimond and check if its movable
                    if [row,col] == Diamonds[i]:
                        for j in range(len(Diamonds)):
                            if [row,col+1] == Diamonds[j]:
                                DimondBlocked=True
                        if col+1 in self.Road[row]: #Road pice after moved
                            if not DimondBlocked: # check for not blocked
                                Diamonds[i]=[row,col+1]
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            self.Player[1]=col

        if self.Player[1] == col:
            return True;
        else:
            return False;
    def left (self):
        row = self.Player[0]
        col = self.Player[1]-1
        DoubleDimond=False
        DimondBlocked=False

        if [row,col] in self.Diamonds:
            # move Diamond
            if [row,col-1] in self.Diamonds:
                DoubleDimond=True
            else:#no dimond besides dimond
                for i in range(len(Diamonds)): #Find dimond and check if its movable
                    if [row,col] == Diamonds[i]:
                        for j in range(len(Diamonds)):
                            if [row,col-1] == Diamonds[j]:
                                DimondBlocked=True
                        if col-1 in self.Road[row]: #Road pice after moved
                            if not DimondBlocked: # check for not blocked
                                Diamonds[i]=[row,col-1]
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            self.Player[1]=col

        if self.Player[1] == col:
            return True;
        else:
            return False;

def init_State( Road, Diamonds, Goals, Player, width):
    state = State(Road, Diamonds, Goals, Player, width)
    return state

game = init_State(RoadAdjencyList,Diamonds,Goals,RobotStart,width)

game.left()
#print game.Player
game.PMap()
game.up()
#print game.Player
game.PMap()
game.up()
#print game.Player
game.PMap()
game.right()
#print game.Player
game.PMap()
game.left()
#print game.Player
game.PMap()
game.down()
#print game.Player
game.PMap()
game.down()
#print game.Player
game.PMap()
game.right()
#print game.Player
game.PMap()

game.up()
#print game.Player
game.PMap()

game.up()
#print game.Player
game.PMap()
############# Check move #########################

############# Class for search queue ###############
import heapq

class PQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements)==0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority,item))

    def get(self):
        return heapq.heappop(self.elements)[1]

############# Game as a class ####################
import copy
class State(object):
    Road = []
    Diamonds = []
    Goals = []
    Player = []
    width=0
    lastposition = (0,0)
    # The class "constructor" - It's actually an initializer
    def __init__(self, Road, Diamonds, Goals, Player, width,lastposition):
        self.Road = Road
        self.Diamonds = Diamonds
        self.Goals = Goals
        self.Player = Player
        self.width= width
        self.lastposition = lastposition

    def getPlayer(self):
        return tuple(self.Player)
    def getDiamonds(self):
        tupleD=()
        for x in self.Diamonds:
            tupleD = tuple(x) + tupleD
        return tupleD
    def getGoals(self):
        tupleD=()
        for x in self.Goals:
            tupleD = tuple(x) + tupleD
        return tupleD

    def getNeigboorsNotLast(self,oldPosition):
        currentN = self.neigboors()
        currentN.remove(oldPosition)
        return currentN
    def neigboors(self):                               # Neeed to reverse moves!=!
        neigboors = []
        y = copy.copy(self.Player[0])
        x = copy.copy(self.Player[1])

        if self.CheckUp():
            neigboors.append(((y-1,x),"up"))

        if self.CheckDown():
            neigboors.append(((y+1,x),"down"))

        if self.CheckLeft():
            neigboors.append(((y,x-1),"left"))

        if self.CheckRight():
            neigboors.append(((y,x+1),"right"))

        return neigboors
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
                for i in range(len(self.Diamonds)): #Find dimond and check if its movable
                    if [row,col] == self.Diamonds[i]:
                        for j in range(len(self.Diamonds)):
                            if [row-1,col] == self.Diamonds[j]:
                                DimondBlocked=True
                        if col in self.Road[row-1]: #Road pice after moved.... NO EXCEPTIon CATCH
                            if not DimondBlocked: # check for not blocked
                                self.Diamonds[i]=[row-1,col]
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            self.Player[0]=row

        if self.Player[0] == row:
            self.lastposition = self.getPlayer()
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
                for i in range(len(self.Diamonds)): #Find dimond and check if its movable
                    if [row,col] == self.Diamonds[i]:
                        for j in range(len(self.Diamonds)):
                            if [row+1,col] == self.Diamonds[j]:
                                DimondBlocked=True
                        if col in self.Road[row+1]: #Road pice after moved.... NO EXCEPTIon CATCH
                            if not DimondBlocked: # check for not blocked
                                self.Diamonds[i]=[row+1,col]
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            self.Player[0]=row

        if self.Player[0] == row:
            self.lastposition = self.getPlayer()
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
                for i in range(len(self.Diamonds)): #Find dimond and check if its movable
                    if [row,col] == self.Diamonds[i]:
                        for j in range(len(self.Diamonds)):
                            if [row,col+1] == self.Diamonds[j]:
                                DimondBlocked=True
                        if col+1 in self.Road[row]: #Road pice after moved
                            if not DimondBlocked: # check for not blocked
                                self.Diamonds[i]=[row,col+1] #Move
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            self.Player[1]=col

        if self.Player[1] == col:
            self.lastposition = self.getPlayer()
            return True;
        else:
            return False;
    def left (self):
        row = self.Player[0]
        col = self.Player[1]-1
        DoubleDimond=False
        DimondBlocked=False

        if [row,col] in self.Diamonds:
            if [row,col-1] in self.Diamonds:
                DoubleDimond=True
            else:#no dimond besides dimond
                for i in range(len(self.Diamonds)): #Find dimond and check if its movable
                    if [row,col] == self.Diamonds[i]:
                        for j in range(len(self.Diamonds)):
                            if [row,col-1] == self.Diamonds[j]:
                                DimondBlocked=True
                        if col-1 in self.Road[row]: #Road pice after moved
                            if not DimondBlocked: # check for not blocked
                                self.Diamonds[i]=[row,col-1]
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            self.Player[1]=col

        if self.Player[1] == col:
            self.lastposition = self.getPlayer()
            return True;
        else:
            return False;

    def CheckUp (self):
        row = self.Player[0]-1
        col = self.Player[1]
        DoubleDimond = False
        DimondBlocked=False
        check = None
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
                                fine=1#Diamonds[i]=[row-1,col] don't move it when check!
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            #self.Player[0]=row on't move it when check!
            check = row

        if check == row:
            return True;
        else:
            return False;
    def CheckDown (self):
        row = self.Player[0]+1
        col = self.Player[1]
        DoubleDimond=False
        DimondBlocked=False
        check = None

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
                                fine=1#Diamonds[i]=[row+1,col]
                        else: #There is a isWall
                            DimondBlocked = True


        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            #self.Player[0]=row
            check = row

        if check == row:
            return True;
        else:
            return False;
    def CheckRight (self):
        row = self.Player[0]
        col = self.Player[1]+1
        DoubleDimond=False
        DimondBlocked=False
        check = None

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
                                fine=1#Diamonds[i]=[row,col+1]
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            #self.Player[1]=col
            check = col

        if check == col:
            return True;
        else:
            return False;
    def CheckLeft (self):
        row = self.Player[0]
        col = self.Player[1]-1
        DoubleDimond=False
        DimondBlocked=False
        check = None

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
                                fine=1#Diamonds[i]=[row,col-1]
                        else: #There is a isWall
                            DimondBlocked = True

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
            #self.Player[1]=col
            check = col

        if check == col:
            return True;
        else:
            return False;
    def SaveState (self):
        return init_State( self.Road ,copy.deepcopy(self.Diamonds),self.Goals,copy.deepcopy(self.Player) ,self.width,copy.deepcopy(self.lastposition))

def init_State( Road, Diamonds, Goals, Player, width,lastposition):
    state = State(Road, Diamonds, Goals, Player, width,lastposition)
    return state

def getPath(came_from, goal):
    current = goal
    path = []
    while current != None:
        path.append(current)
        current = came_from[current]
    return path

########### H
def H(Diamonds, Goals):
    D = [] # Y1,X1
    G = [] # Y2,X2
    a=0

    for i in range(len(Diamonds)-1):
        D.append([Diamonds[i],Diamonds[i+1]])
        G.append([Goals[i],Goals[i+1]])

    for i in range(len(Diamonds)):
        a = abs(Diamonds[i] - Goals[i]) + a
    print "TXT: ", a
    print "TXT: ", D
    print "TXT: ", G
    return a

######################## Search #########################
def justSearch(game):
    print "\n===== Search start =========\n"
    #nGoals
    goals = game.Goals
    # Init Priot Queue
    Q = PQueue()
    Q.put(game,0)   # Item, prioty
    # Init path and cost dictonaries
    came_from  = {} # Create dictonary
    cost_so_far = {}
    pseudoState=(game.getPlayer(),game.getDiamonds())
    came_from[ pseudoState ]  = None # tuple player & diamonds position
    cost_so_far[game.getPlayer()] = 0

    while not Q.empty():
        currentState = Q.get()
        print "\nCurrentState map:"
        currentState.PMap()
        print "\nChecking diamonds == goals: \n", currentState.Diamonds , " == ", goals
        if currentState.Diamonds == goals:    # Need to implement sevelreal goals
            print "------------ Yes, congratz!------------"
            with open("path.txt", "w+") as pathFile:
                pathFile.write("Came from\n")
                pathFile.write(str(getPath(came_from,(currentState.getPlayer(),currentState.getGoals() ) )))
                pathFile.write("\nCost:\n")
                pathFile.write(str(cost_so_far[currentState.getPlayer()]))
            break
        print "False."
        print "\nCurrentState neigboors: \n", currentState.neigboors()
        lastpseudoState = (copy.deepcopy(currentState.getPlayer()),copy.deepcopy(currentState.getDiamonds()) )
        for next in currentState.neigboors():
            print "     Current positin: ", currentState.getPlayer()                           #TODO: Check that next state is not the same as before, unless a dimond is moved.
            print "     Child position: ", next[0], " Direction: ", next[1]
            Direction = next[1]
            NewGame = currentState.SaveState()
            new_cost = cost_so_far[currentState.lastposition] +1
            # Direction control
            if Direction == "up":
                print "     Went up"
                NewGame.up()
            elif Direction == "down":
                print "     Went down"
                NewGame.down()
            elif Direction == "right":
                print "     Went right"
                NewGame.right()
            elif Direction == "left":
                print "     Went left"
                NewGame.left()
            else:
                print "!! ERROR 01: next[1] was a Unvalid direction !!"

            if NewGame.getDiamonds() == NewGame.getPlayer():
                print "Went right ERROR: NewGame diamonds: ", NewGame.getDiamonds(), " and ", NewGame.getPlayer()
                print "=============================================================================================================="
                NewGame.PMap()

            print "     == New state: =="
            NewGame.PMap()
            pseudoState=(NewGame.getPlayer(),NewGame.getDiamonds())

            print "\n     New state pseudoState: ", pseudoState
            print "     Came_from: ",lastpseudoState
            # print"     ",came_from
            if pseudoState not in came_from or new_cost < cost_so_far[NewGame.getPlayer()]:
                cost_so_far[NewGame.getPlayer()] = new_cost
                priority = new_cost + H(NewGame.getDiamonds(),NewGame.getGoals())
                print "          Putted in to Q: ", NewGame.getPlayer()
                Q.put(NewGame,priority) #Item, priority
                came_from[pseudoState] = lastpseudoState
            else:
                print "          Already in Q, Pseudostate :", pseudoState
            del NewGame
    print "\n===== Search finish =========\n"
    return came_from, cost_so_far

############## Global sh* ##########
## File manipulation ######
f =open("simpleMap.txt","r")
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



def main():
    game = init_State(RoadAdjencyList,Diamonds,Goals,RobotStart,width,tuple(RobotStart))
    ######################## Test #########################


    came, cost = justSearch(game)


    # print "came: ", came
    # print "cost: ", cost

    #print "Path: \n", getPath(came,None,)

    ##Solution
    # game.down()
    # game.PMap()
    # print game.neigboors()
    # game.right()
    # game.PMap()


    print "\nTO do:"
     print "* Make heuristik improvement."
    # print "* game.up in dsearch check if valid"
    # print "* Moved a dimond last time"

    #OutPut
    #L=left
    #R=right
    #F=front
    #B=back
    #['']

if __name__ == '__main__':
    main()

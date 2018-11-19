######### File manipulation ###############
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
    def getPlayer(self):
        return tuple(self.Player)

    def getNeigboorsNotLast(self,oldPosition):
        currentN = self.neigboors()
        currentN.remove(oldPosition)
        return currentN

    def neigboors(self):                               # Neeed to reverse moves!=!
        neigboors = []

        if self.CheckUp():
            neigboors.append(((self.Player[0]-1,self.Player[1]),"up"))

        if self.CheckDown():
            neigboors.append(((self.Player[0]+1,self.Player[1]),"down"))

        if self.CheckLeft():
            neigboors.append(((self.Player[0],self.Player[1]-1),"left"))

        if self.CheckRight():
            neigboors.append(((self.Player[0],self.Player[1]+1),"right"))

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

        if col in self.Road[row] and not DoubleDimond and not DimondBlocked:
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
        return init_State(self.Road,self.Diamonds,self.Goals,self.Player,self.width)

def init_State( Road, Diamonds, Goals, Player, width):
    state = State(Road, Diamonds, Goals, Player, width)
    return state

game = init_State(RoadAdjencyList,Diamonds,Goals,RobotStart,width)

######################## move #########################
#
# game.left()
# # print game.Player
# game.PMap()
# game.up()
# # print game.Player
# game.PMap()
# game.up()
# # print game.Player
# game.PMap()
# game.right()
# game.PMap() #!!! ERROR Diamond through wall!=!
# print "=======================================\n"
# print "=======================================\n"
###################### Search ###############################
def dsearch(game):
    graph = tuple(self.Road)
    start = tuple(self.Player)
    goal = tuple(goalToT)
    frontier = PQueue()
    frontier.put(self,0) #Item, prioty
    print "Starting in: ", start
    came_from = {}
    cost_so_far={}
    came_from[start] = 0
    cost_so_far[start]= 0

    NewGame = init_State(self.Road,self.Diamonds,self.Goals,self.Player,self.width)


    while not frontier.empty():
        current = frontier.get()
        print "Current: ", current.PMap()

        if current ==  goal:
            print "Goal: ", current, " == ", goal
            break

        print "Print neigboors: ", self.neigboors()
        for next in self.neigboors():

            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next,priority) #Item, priority
                came_from[next] = current

    return came_from, cost_so_far

def justSearch(game):
    #nGoals
    goals = game.Goals
    # Init Priot Queue
    Q = PQueue()
    Q.put(game,0)   # Item, prioty
    # Init path and cost dictonaries
    came_from  = {} # Create dictonary
    cost_so_far= {}
    came_from[game.getPlayer()] = 0 # tuple player position
    cost_so_far[game.getPlayer()]= 0
    gamelist=[]


    while not Q.empty():
        currentState = Q.get()
        print "\nCurrentState map:"
        currentState.PMap()

    print "\nIs diamonds: ", currentState.Diamonds , " == ", goals
    if currentState.Diamonds == goals:    # Need to implement sevelreal goals
        print "Yes, congratz!"
        pass

    print "\nCurrentState neigboors: ", currentState.neigboors()
    for next in currentState.neigboors():
        print "     Child position: ", next[0], " Direction: ", next[1]
        Direction = next[1]
        NewGame = currentState.SaveState()
        if Direction == "up":
            print "     Went up"
        elif Direction == "down":
            print "     Went down"
        elif Direction == "right":
            print "     Went right"
        elif Direction == "left":
            print "     Went left"
        else:
            print "ERROR 01: next[1] was a Unvalid direction"


    print "\n===== Search finish =========\n"
    return came_from

print justSearch(game)

print "\nTO do:"
print "* Implent move in search to get new neighboors"
print "* Implent move in search to get new neighboors"
#Came,Cost = game.dsearch([6,3])
#print "Came: ", Came
#print "Cost: ", Cost

#OutPut
#L=left
#R=right
#F=front
#B=back
#['']

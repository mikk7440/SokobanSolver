######### File manipulation ###############
f =open("map.txt","r")
Data = f.readlines()
Data = [x.strip('\n') for x in Data]
f.close()

############# Print Map function #########################
def PrintMap (width, Road, Diamond, Goals, Player):
    line = ""
    R = 0 # Road
    supR = 0 # Sup Road
    D = 0 #Diamond counter
    G = 0 # Goals
    P = 0 # Robot player
    nextChar = ''


    for i in range(len(Road)-1):
        for j in range(width):

            while len(Road[R]) == 0:
                R+=1
                supR=0

            if Road[R][0][supR] == j and R == i:
                nextChar='.'
                if supR < len(Road[R][0])-1:
                    supR+=1
                else:
                        R+=1
                        supR=0

            if Diamond[D] == [i,j]:
                nextChar='J'
                if D < len(Diamond)-1:
                    D+=1

            if Goals[G] == [i,j]:   # Need to handle when goal is under player/
                nextChar='G'
                if G < len(Goals)-1:
                    G+=1
            if nextChar=='':
                nextChar='X'

            line+=nextChar
            nextChar =''
        print(line)
        line = ""
        L = 0
    return;

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
RobotStart = []
list = []

# Check if walkaable field or X, save Road, Diammond etc.
for i in range(len(Data)):
    for j in range(len(Data[i])):
        if  Data[i][j] == isRoad:
            list.append(j)
        elif Data[i][j] == isDiamond:
            Diamonds.append([i,j])
            list.append(j)
        elif Data[i][j] == isGoal:
            Goals.append([i,j])
            list.append(j)
        elif Data[i][j] == isRobotStart:
            RobotStart.append([i,j])
            list.append(j)
    if len(list)!= 0 :
        RoadAdjencyList[i].append(list)
    list = []


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

PrintMap(width,RoadAdjencyList,Diamonds,Goals,RobotStart)
print width
############# Check move #########################

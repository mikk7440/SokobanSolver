######### File manipulation ###############
f =open("map.txt","r")
Data = f.readlines()
Data = [x.strip('\n') for x in Data]
f.close()

############# Print Map function #########################
def PrintMap (width, Road, Diamond, Goals, Robot):
    line = ""
    L = 0
    D = 0
    G = 0
    R = 0
    for i in range(len(Road)):
        for j in range(width):
            if j < len(Road)-1:
                #if Road[i][0][L] == j:
                #    line+='.'
                #    print( len(Road[i][0])-1)

                if Diamond[D] == [i,j]:
                    line+='J'
                    if D < len(Diamond)-1:
                        D+=1
                else:
                    line+='X'
            else:
                line+='X'
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

############# Check move #########################

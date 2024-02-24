import random
import math

#######################################################

###########################
#                         #
#   POLYNOMIAL FUNCTION   #
#                         #
###########################

def fitness(x):
    X = x[0] + x[1] * 1j
    f = X**5 + 1/2 * X**3 - 2 * X**2 + X + 15
    return abs(f)

#######################################################

#######################
#                     #
#      VARIABLES      #
#                     #
#######################

MAX_VAL = 10
MIN_VAL = -10
PRECISION = 5
USE_DEFAULTS = False
ECHO_CONV = True

b = 0.4
r = -1
mothsNum = 50
flamesNum = 0
itNum = 2000

#######################################################
        
#########################################
#                                       #
#   MOTH-FLAME OPTIMIZATION ALGORITHM   #
#                                       #
#########################################

def MFO():
    moths = InitMoths(mothsNum)
    flames = moths.copy()
    flames.sort(key = SortKey)
    global flamesNum
    global r
    l = 0
    conv = 0
    while l < itNum:
        flamesNum = round(mothsNum - l*(mothsNum - 1)/itNum)
        r = -l/itNum - 1
        for i in range(0, mothsNum):

            j = i
            if(j >= flamesNum):
                j = flamesNum - 1
            
            for k in range(len(moths[i].x)):
                moths[i].x[k] = S(moths[i].x[k], flames[j].x[k])
            moths[i].val = fitness(moths[i].x)
        UpdateFlames(moths, flames)
        
        if len(Unique(flames[0:flamesNum-1])) == 1:
            conv = conv + 1
        if conv > 2 and ECHO_CONV:
            print("convergence after", l, "iterations")
            break

        l = l+1

    return RoundMoth(moths[0])

def InitMoths(mothsNum):
    moths = []
    for i in range(mothsNum):
        moths.append(Moth(2))
    return moths

def UpdateFlames(moths, flames):
    temp = moths.copy()
    temp.sort(key=SortKey)
    i = j = 0
    while j < flamesNum:
        if temp[i].val < flames[j].val:
            flames[j] = temp[i]
            i = i+1
        j = j+1

def S(M, F):
    D = abs(F-M)
    t = random.uniform(r, 1)
    return D * math.exp(b * t) * math.cos(2 * math.pi * t) + F

class Moth:
    x = []
    val = -1

    def __init__(self, varNum) -> None:
        self.x = random.sample(range(MIN_VAL, MAX_VAL), varNum)
        self.val = fitness(self.x)

    def __str__(self) -> str:
        return f"{self.x}"

#######################################################

##############################
#                            #
#      HELPER FUNCTIONS      #
#                            #
##############################

def SortKey(m):
    return m.val

def RoundMoth(m):
    for i in range(len(m.x)):
        m.x[i] = round(m.x[i], PRECISION)
    m.val = fitness(m.x)
    return m

def Equal(m1, m2):
    if len(m1.x) != len(m2.x):
        return False
    for i in range(len(m1.x)):
        if m1.x[i] != m2.x[i]:
            return False
    return True

def Unique(moths):
    unique = []

    for m in moths:
        not_unique = False
        for u in unique:
            if Equal(m, u):
                not_unique = True
                break
        if not not_unique:
            unique.append(m)

    return unique

#######################################################

########################
#                      #
#         MAIN         #
#                      #
########################

def main():
    global mothsNum
    global itNum
    global b

    if USE_DEFAULTS:
        trials = 30
    else:
        while True:
            mothsNum = int(input("Number of moths: "))
            if mothsNum > 0:
                break
        
        while True:
            itNum = int(input("Max iterations: "))
            if itNum > 0:
                break
        
        b = float(input("Shape constant: "))

        while True:
            trials = int(input("Number of trials: "))
            if trials > 0:
                break

    results = []

    for i in range(trials):
        results.append(MFO())
    
    results = Unique(results)
    print("\nResults:")
    for r in results:
        print(r)

main()
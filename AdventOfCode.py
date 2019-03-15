#this file solves the advent of code problem: 2016/day 11
# It starts with calling the function solve() and passing it the initial state of the floors, and the position of elevator
# solve() takes the initial state and generates successors for it.
# All the successors are placed on a fringe.
# Using the concept of BFS, the successors are popped from the fringe one by one along the breadth of the decision tree.
# Each pooped successor is passesd to the successors() and its successors are generated.
# Solve() also has a list called visited which maintains the successors explored in the past and pruns their exploration again


def solve(initial_state):
    fringe = [initial_state]
    prune_count = 0
    floor = [3]
    steps = [0]
    goals = []
    visited = []
    steps_visited = []
    while len(fringe) > 0:
        #print ("Inside solve->while")
        curr_state = fringe.pop(0)
        curr_floor=floor.pop(0)
        curr_steps = steps.pop(0)
        print "\n CURRENT::", curr_state, " FLOOR::", curr_floor
        #visited.append([insertIntoVisited(curr_state, curr_floor), curr_floor])
        visited.append([pairUp(curr_state), curr_floor])
        steps_visited.append(curr_steps)
        for s in successors(curr_state, curr_floor, curr_steps):
            if not inVisited(s[0], visited, s[1]):
                if not inFringe(s[0], fringe, s[1], floor):
                    if is_goal(s[0]):
                        goals.append(s)
                        return goals
                    else:
                        fringe.append(s[0])
                        floor.append(s[1])
                        steps.append(s[2])
                # else:
                #     pos = fringe.index(s[0])
                #     if s[1] == floor[pos]:
                #         if s[2] < steps[pos]:
                #             steps[pos] = s[2]
                #     else:
                #         fringe.append(s[0])
                #         floor.append(s[1])
                #         steps.append(s[2])
                        #floor[pos] = s[1]
        #print "\n VISITED:", visited
        print "\n FRINGE SIZE:",len(fringe)
        print "GOAL:::",goals
    return goals


# This function generates a list whose each element is the combination of row numbers for one pair of generator and microchip on the current state 'curr'
def pairUp(curr):
    lis = []
    res = []
    for j in range(0,len(curr[0])):
        for i in range(0,len(curr)):
            if curr[i][j] == 1:
                lis.append(i)
                break
        if len(lis) == 2:
            res.append(lis)
            lis = []
    return res


# This function checks if the current state 'curr' is present on the fringe with their elevators being on the same floors as well.
def inFringe(curr, fringe, f, floor):
    lis1 = pairUp(curr)
    for i in range(0, len(fringe)):
        if floor[i] == f:
            lis2 = pairUp(fringe[i])
            for ele in lis1:
                if ele in lis2:
                    lis2.remove(ele)
            if lis2 == []:
                return True
    return False


# This function checks if the current state 'curr' already exits in the visited list 'visited_lis' with elevator being on the same floor for both.
def inVisited(curr, visited_lis, f):
    lis1 = pairUp(curr)
    for i in range(0,len(visited_lis)):
        if visited_lis[i][1] == f:
            lis2 = visited_lis[i][0][0:]
            for ele in lis1:
                if ele in lis2:
                    lis2.remove(ele)
            if lis2 == []:
                return True
    return False


# This function checks is the state is a goal state. If yes, it returns a True else it returns a false
def is_goal(state):
    if sum(state[0]) == len(state[0]):
        if sum(state[1]) == 0 and sum(state[2]) == 0 and sum(state[3]) == 0:
            return True
    return False


# successors(curr, floor, steps)
#       : this functions calculates the successors of the current state 'curr'.
#       : Input arguments are current state, the current floor where elevator is parked, number of steps taken till now
#       : It returns a set of successors of curr along with the location of elevator and number of steps till that successor
def successors(curr, floor, steps):
    successors = []
    if floor > 0:                                              #When the elevator goes up
        for j in range(0, len(curr[floor])):
            elevator = []
            if curr[floor][j]:
                elevator.append(j)
                if isCompatible(elevator, curr[floor-1]):
                    if floor == 1:
                        succ = [curr[floor-1][0:j]+[curr[floor][j],]+curr[floor-1][j+1:]] + [curr[floor][0:j]+[0,]+curr[floor][j+1:]] + curr[floor+1:]
                    else:
                        succ = curr[0:floor-1]+ [curr[floor-1][0:j]+[curr[floor][j],]+curr[floor-1][j+1:]] + [curr[floor][0:j]+[0,]+curr[floor][j+1:]] + curr[floor+1:]
                    successors.append([succ, floor-1, steps+1])
                    print("SUCCESSOR 1::",succ,floor-1, steps+1)
                for i in range(j+1, len(curr[floor])):
                    if curr[floor][i] and isCompatible(elevator, [curr[floor][i]]):
                        elevator.append(i)
                        if isCompatible(elevator, curr[floor-1]):
                            if floor == 1:
                                succ = [curr[floor - 1][0:j] + [curr[floor][j], ] + curr[floor - 1][j+1:i] + [curr[floor][i],] + curr[floor-1][i+1:] ] + [curr[floor][0:j] + [0,] + curr[floor][j+1:i] + [0,] + curr[floor][i+1:]] + curr[floor+1:]
                            else:
                                succ = curr[0:floor-1]+ [curr[floor-1][0:j]+[curr[floor][j],]+curr[floor-1][j+1:i] + [curr[floor][i], ] + curr[floor-1][i+1:]] + [curr[floor][0:j] + [0,] + curr[floor][j+1:i] + [0,] + curr[floor][i+1:]] + curr[floor+1:]
                            successors.append([succ, floor-1, steps+1])
                            print("SUCCESSOR 2::",succ, floor-1, steps+1)
                        elevator.pop()

   # if floor < 3:                                               #When the elevator goes down
    if floor<3 and (sum(curr[floor+1]) or len(successors) == 0):
        for j in range(0, len(curr[floor])):
            elevator = []
            if curr[floor][j]:
                elevator.append(j)
                if isCompatible(elevator, curr[floor + 1]):
                    if floor == 2:
                        succ = curr[0:floor] + [curr[floor][0:j] + [0, ] + curr[floor][j + 1:]] + [curr[floor+1][0:j] + [curr[floor][j], ] + curr[floor+1][j + 1:]] # + curr[floor + 2:]
                    else:
                        succ = curr[0:floor] + [curr[floor][0:j] + [0, ] + curr[floor][j + 1:]] + [curr[floor + 1][0:j] + [curr[floor][j], ] + curr[floor + 1][j + 1:]]  + curr[floor + 2:]
                    successors.append([succ, floor+1, steps+1])
                    print("SUCCESSOR 3::",succ, floor+1, steps+1)
                for i in range(j+1, len(curr[floor])):
                    if curr[floor][i] and isCompatible(elevator, [curr[floor][i]]):
                        elevator.append(i)
                        if isCompatible(elevator, curr[floor+1]):
                            if floor == 2:
                                succ = curr[0:floor] + [curr[floor][0:j] + [0, ] + curr[floor][j + 1:i] + [0,] + curr[floor][i+1:]] + [curr[floor + 1][0:j] + [curr[floor][j], ] + curr[floor + 1][j + 1:i] + [curr[floor][i], ] + curr[floor + 1][i + 1:]]  # + curr[floor + 2:]
                            else:
                                succ = curr[0:floor] + [curr[floor][0:j] + [0, ] + curr[floor][j + 1:i] + [0,] + curr[floor][i+1:]] + [curr[floor + 1][0:j] + [curr[floor][j], ] + curr[floor + 1][j + 1:i] + [curr[floor][i], ] + curr[floor + 1][i + 1:]] + curr[floor + 2:]
                            successors.append([succ, floor+1, steps+1])
                            print("SUCCESSOR 4::",succ, floor+1, steps+1)
                        else:
                            elevator.pop()
    return successors


# isCompatible(elevator, floor)
#     : it checks if the elevator is compatible with elements on next floor if elevator elements is/are moved to the next floor
#     : elevator is the list of elements that we are moving to say floor F
#     : floor is the list of elements on floor F
def isCompatible(elevator, floor):
    i = 0
    evens = []
    odds = []
    while i<len(floor):
        if floor[i]:
            if i % 2 == 0:
                if i+1 < len(floor) and floor[i+1]:
                    i += 2
                    continue
                evens.append(i)
            else:
                odds.append(i)
        i += 1
    for ele in elevator:
        if ele%2 :
            if ele-1 not in elevator and len(evens) and evens != [ele-1]:
                return False
        elif ele%2 ==0 :
            if ele+1 not in elevator and len(odds) and odds != [ele+1]:
                return False
    return True


#initial_state = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1], [1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0]]
initial_state = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]]
solution = solve(initial_state)
print "SOLUTION",solution

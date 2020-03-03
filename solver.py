import rubik

def apply_all_perms(position):
    perms = []
    for move in rubik.quarter_twists_names:
        perms.append(rubik.perm_apply(move, position))
    return perms

def construct_path(overlap, Ldict, Rdict):
    #need to be a list of moves
    Lpath = [overlap]
    Rpath = [Rdict[overlap][2]]
    while True:
        pass
    return Lpath + Rpath


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    Ldict = { start : ("s", None) }
    LQueue = [start]
    Lcount = 1
    Rdict = { end : ("e", None) }
    RQueue = [end]
    Rcount = 1
    overlap = tuple()
    while True:
        newLCount = 0
        for i in range(Lcount):
            if LQueue[i] in Rdict:
                overlap = LQueue[i]
                break
            else:
                perms = apply_all_perms(LQueue[i])
                for i in range(len(perms)):
                    if perms[i] not in Ldict:
                        Ldict[perms[i]] = (rubik.quarter_twists_names[i], perms[i])
                        LQueue.append(perms[i])
                        newLCount+=1
        Lcount = newLCount
        newRCount = 0
        for i in range(Rcount):
            if RQueue[i] in Ldict:
                overlap = RQueue[i]
                break
            else:
                perms = apply_all_perms(RQueue[i])
                for i in range(len(perms)):
                    if perms[i] not in Rdict:
                        Rdict[perms[i]] = (rubik.quarter_twists_names[i], perms[i])
                        RQueue.append(perms[i])
                        newRCount+=1
        Rcount = Lcount
        
    #construct path if an overlap is found
    path = []
    if overlap:
        path = construct_path(overlap, Ldict, Rdict)
    return path

if __name__ == "__main__":
    start = (6, 7, 8, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23)
    end = rubik.I
    result = shortest_path(start, end)
import rubik

def construct_path(overlap, Ldict, Rdict):
    # prepend moves to left list
    # append moves to right list
    Lpath = []
    Rpath = []
    Lcurr = overlap
    Rcurr = overlap
    while True:
        if Ldict[Lcurr][0] == 's':
            break
        Lpath.insert(0, Ldict[Lcurr][0])
        Lcurr = Ldict[Lcurr][1]
    while True:
        if Rdict[Rcurr][0] == 'e':
            break
        Rpath.append(Rdict[Rcurr][0])
        Rcurr = Rdict[Rcurr][1]
    
    return Lpath + Rpath


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    # dict: 
    # key = current configuration
    # value = (move, parent's configuration)
    Ldict = { start : ("s", None) }
    LQueue = [start]
    Lcount = 1
    Rdict = { end : ("e", None) }
    RQueue = [end]
    Rcount = 1
    overlap = tuple()
    depth = 0
    while True:
        if depth > 7:
            print("Error: Invalid configuration")
            return None
        newLCount = 0
        for i in range(Lcount):
            curr = LQueue.pop(0)
            if curr in Rdict:
                overlap = curr
                return construct_path(overlap,Ldict, Rdict)
            else:
                for move in rubik.quarter_twists:
                    perm = rubik.perm_apply(move, curr)
                    if perm not in Ldict:
                        Ldict[perm] = (move, curr)
                        LQueue.append(perm)
                        newLCount+=1
        Lcount = newLCount
        newRCount = 0
        for i in range(Rcount):
            curr = RQueue.pop(0)
            if curr in Ldict:
                overlap = curr
                return construct_path(overlap, Ldict, Rdict)
            else:
                for move in rubik.quarter_twists:
                    perm = rubik.perm_apply(move,curr)
                    if perm not in Rdict:
                        Rdict[perm] = (move, curr)
                        RQueue.append(perm)
                        newRCount+=1
        Rcount = newRCount
        depth+=1
    # end while
    return None

"""
if __name__ == "__main__":
    start = (6, 7, 8, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23)
    end = rubik.I
    result = shortest_path(start, end)
"""
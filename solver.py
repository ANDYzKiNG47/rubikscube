import rubik

"""
invariant: Lpath stores the path to the overlap and Rpath stores the inverse moves to end
"""
def construct_path(overlap, Ldict, Rdict):

    Lpath = []
    Rpath = []
    Lcurr = overlap
    Rcurr = overlap
    # starting with overlap, prepend moves to the left list until the start is found
    while True:
        if Ldict[Lcurr][0] == 's':
            break
        Lpath.insert(0, Ldict[Lcurr][0])
        Lcurr = Ldict[Lcurr][1]
    # starting with overlap, append inverse moves to the right list until the end is found
    while True:
        if Rdict[Rcurr][0] == 'e':
            break
        Rpath.append(rubik.perm_inverse(Rdict[Rcurr][0]))
        Rcurr = Rdict[Rcurr][1]
    # return right list appended to left list for the complete moveset
    return Lpath + Rpath


def shortest_path(start, end):
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
    '''
    invariant: both queues will always store the configurations of the previous depth's permuations
    
    invariant: if a configuration that exists in a queue, as well as the oposite side's dictionary,
    then there must exist a path from start to finish of length depth
    '''
    '''
    Initialization: LQueue stores the start config and RQueue Stores the end config
    
    Mainenance: All permuations of the current configuration are stored in their respective dictionaries,
    and checked against the oposite diction to check for overlaps. Unique permuations are stored in their
    respective queues to create new permutations at the next depth if no overlap is found
    
    Termination: an overlap is found, meaning there exists a path from start to finish of length depth,
    or depth 7 of the BFS is reached meaning no path exists from start to finish.
    '''
    while True:
        # if depth > 7 then the cube has an invalid configuration and there is no solution
        if depth > 7:
            return None
        newLCount = 0
        # find all permuations of all the configurations in the left queue
        for i in range(Lcount):
            curr = LQueue.pop(0)
            # if an overlap is found
            if curr in Rdict:
                overlap = curr
                return construct_path(overlap, Ldict, Rdict)
            else:
                # add all permuations of the current configuration to the queue
                for move in rubik.quarter_twists:
                    perm = rubik.perm_apply(move, curr)
                    # add all the permuations of the current configuration to the Ldict if not already in there
                    if perm not in Ldict:
                        Ldict[perm] = (move, curr)
                        LQueue.append(perm)
                        newLCount+=1
        Lcount = newLCount
        newRCount = 0
        for i in range(Rcount):
            curr = RQueue.pop(0)
            # if an overlap is found
            if curr in Ldict:
                overlap = curr
                return construct_path(overlap, Ldict, Rdict)
            else:
                # add all permuations of the current configuration to the queue
                for move in rubik.quarter_twists:
                    perm = rubik.perm_apply(move, curr)
                    # add all the permuations of the current configuration to the Ldict if not already in there
                    if perm not in Rdict:
                        Rdict[perm] = (move, curr)
                        RQueue.append(perm)
                        newRCount+=1
        Rcount = newRCount
        depth+=1
    # end while
    return None



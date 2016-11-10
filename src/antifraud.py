import sys
inFile1 = sys.argv[1]
inFile2 = sys.argv[2]
outFile1 = sys.argv[3]
outFile2 = sys.argv[4]
outFile3 = sys.argv[5]


# use two level hash table to store data
# friend[id1][id2] = 1 means they have payments
# the time complexity of checking whether two ids are "1st degree friend" is O(1) 
friend = dict()
count = 0
with open(inFile1, 'r') as f:
    next(f)   # skip header
    for line in f:        
        info = line.split(',')
        if len(info) > 3:   # consider only valid lines which contain at least 3 columns
            id1 = info[1]
            id2 = info[2]
            if id1 not in friend:
                friend[id1] = dict()
                friend[id1][id2] = 1
            elif id2 not in friend[id1]:
                friend[id1][id2] = 1
            if id2 not in friend:
                friend[id2] = dict()
                friend[id2][id1] = 1
            elif id1 not in friend[id2]:
                friend[id2][id1] = 1


### feature 1
# for a new payment, we just need to check whether they had a transaction with
# each other from the friend dictionary, the time complexity is O(1)
def feature1(line, friend):
    info = line.split(',')
    if len(info) > 3:
        id1 = info[1]
        id2 = info[2]
        if id1 not in friend or id2 not in friend:
            return False
        elif id2 in friend[id1]:
            return True
    else:
        return False

with open(inFile2, 'r') as f:
    with open(outFile1, 'w') as output:
        next(f)   # skip header
        for line in f:
            if feature1(line, friend):
                output.write('trusted\n')
            else:
                output.write('unverified\n')


# feature 2
# for a new payment, we first check whether they are "1st degree friend", if not then
# check whether they are "2nd degree friend" by iterating all "1st friend" of 
# one person, the time complexity is O(n) where n is number of friends of a person
def feature2(line, friend):
    info = line.split(',')
    if len(info) > 3:
        id1 = info[1]
        id2 = info[2]
        if id1 not in friend or id2 not in friend:
            return False
        elif id2 in friend[id1]:
            return True
        else:
            for i in friend[id1].keys():
                if id2 in friend[i]:
                    return True
    else:
        return False

with open(inFile2, 'r') as f:
    with open(outFile2, 'w') as output:
        next(f)   # skip header
        for line in f:
            if feature2(line, friend):
                output.write('trusted\n')
            else:
                output.write('unverified\n')


# feature 3
# similar to feature 3, for a new payment, we first check whether they are 
# "1st friend", if not then check "2nd degree", if not then check "3rd degree"
# if not then "4th degree" through iteration
# add a searched dictionary to store friends we have checked in lower degree so 
# we will not need to search again in higher degree
# the time complexity of the worst case is O(n^4) where n is number of 
# friends of a person, however on average it is much faster
def feature3(line, friend, searched):
    info = line.split(',')
    if len(info) > 3:   # valid lines
        id1 = info[1]
        id2 = info[2]
        if id1 not in friend or id2 not in friend:
            return False
        elif id2 in friend[id1]:
            return True
        else:
            for i in friend[id1].keys():
                if id2 in friend[i]:
                    return True
                else:
                    for j in friend[i].keys():
                        if j in searched:
                            continue
                        elif id2 in friend[j]:
                            return True
                        else:
                            for k in friend[j].keys():
                                if id2 in friend[k]:
                                    return True
                        searched[j] = 1
                searched[i] = 1
            return False
    else:   # invalid lines
        return False

with open(inFile2, 'r') as f:
    with open(outFile3, 'w') as output:
        next(f)   # skip header
        for line in f:
            searched = dict()   # store searched elements
            if feature3(line, friend, searched):
                output.write('trusted\n')
            else:
                output.write('unverified\n')
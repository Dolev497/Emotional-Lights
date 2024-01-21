import copy
'''def initiate_splitty(Ranks, listy, additionals):
    splitted_list = [[]]*(additionals+len(listy))
    pasts = []
    for cuts in range(additionals):
        minlist = [min(x) for x in Ranks]
        currentmin = min(minlist)
        print(currentmin)
        currentminindex = (minlist.index(currentmin), Ranks[minlist.index(currentmin)].index(currentmin))
        bias = len([x for x in pasts if x <= currentminindex[0]])                 
        pasts.append(currentminindex[0])
        splitted_list[currentminindex[0]+bias] = listy[currentminindex[0]][:currentminindex[1]+1]
        splitted_list[currentminindex[0]+bias+1] = listy[currentminindex[0]][currentminindex[1]+1:]
        Ranks[currentminindex[0]][currentminindex[1]] = 100
        if Ranks[currentminindex[0]] == []:
            Ranks.pop(currentminindex[0])
        print(splitted_list)'''

#initiate_splitty([[0.2, 0.3 , 0.4], [0.9]], [[1, 2, 4], [5, 6]], 3)
def listcutplz(listy= [1,2,3,4], indexes= [0,1,2]):
    submit = []
    if indexes == []:
        return [listy]
    index = indexes[0]
    submit.append(listy[:index+1])
    temp = listcutplz(listy[index+1:], [x-index-1 for x in indexes[indexes.index(index)+1:]])
    submit.extend(temp)
    return submit

def yipeee(x):
    return x[0]+(x[1]/100)

def initiate_splittys(Ranks, listy, additionals):
    splitted_list = [[]]*(additionals+len(listy))
    cut_indexes = []
    for cuts in range(additionals):
        minlist = [min(x) for x in Ranks]
        currentmin = min(minlist)
        currentminindex = (minlist.index(currentmin), Ranks[minlist.index(currentmin)].index(currentmin))
        cut_indexes.append(currentminindex)
        Ranks[currentminindex[0]][currentminindex[1]] = 100
    print(cut_indexes)
    cut_indexes.sort(key= yipeee)
    print(cut_indexes)
    MALIST  = []
    for section in range(len(listy)):
        tempcuts = [x[1] for x in cut_indexes if x[0] == section]
        print(tempcuts)
        MALIST.extend(listcutplz(listy[section], tempcuts))
    return MALIST
'''
    minlist = [min(x) for x in Ranks]
    currentmin = min(minlist)
    print(currentmin)
    
    bias = len([x for x in pasts if x <= currentminindex[0]])                 
    pasts.append(currentminindex[0])
    splitted_list[currentminindex[0]+bias] = listy[currentminindex[0]][:currentminindex[1]+1]
    splitted_list[currentminindex[0]+bias+1] = listy[currentminindex[0]][currentminindex[1]+1:]
    
    if Ranks[currentminindex[0]] == []:
        Ranks.pop(currentminindex[0])
'''
if __name__ == "__main__":
    print(initiate_splittys([[0.2, 0.3], [0.4]], [[1, 2, 4], [5, 6]], 3))

from string import printable as char_set
from random import choices, randint

def genRandString(strLen : int) -> str:
    assert strLen > 0
    return ''.join(choices(char_set, k=strLen))

def genRandStringRange(minLen : int, maxLen : int) -> str:
    return genRandString(randint(minLen, maxLen))

def genRandList(listLen : int, strLen : int, maxStrLen : int = 0) -> list[str]:
    if maxStrLen == 0: maxStrLen = strLen

    return list(set(genRandStringRange(strLen, maxStrLen) for _ in range(listLen)))

def genSortedList(listLen : int, strLen : int, maxStrLen : int = 0) -> list[str]:
    # removed cus lwk i tried to be smart and time efficient but i dont think it is properly random
    # it's here cus i was too proud of my possible smartness to remove this, even tho it ended up bombing 😭🥀
    # 
    # sortedList : list[str]

    # if listLen < len(char_set):
    #     sortedList = char_set[:listLen]
    # else:
    #     sortedList = char_set
    #     for newLength in range(len(char_set), listLen):
    #         index = randint(0, newLength - 1)
    #         sortedList.insert(index, sortedList[index])
    
    # if strLen == 1 and maxStrLen == 1:
    #     return sortedList
    # else:
    # 

    return sorted(genRandList(listLen, strLen, maxStrLen))

def genNearlySortedList(listLen : int, strLen : int, maxStrLen : int = 0, amtSwappedPairs : int = 0) -> list[str]:
    assert amtSwappedPairs > 0

    sortedList = genSortedList(listLen, strLen, maxStrLen)

    for _ in range(amtSwappedPairs):
        firstIndex, secondIndex = randint(0, listLen - 1), randint(0, listLen - 1)

        sortedList[firstIndex], sortedList[secondIndex] = sortedList[secondIndex], sortedList[firstIndex]

    return sortedList

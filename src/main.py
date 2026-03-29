from trees.LLRBBST import LLRBBST
from trees.twothreetree import two_three_tree as TWO_THREE
from datagenfuncs import genRandList, genSortedList, genNearlySortedList

from timeit import timeit

DATASET_SIZES : list[int] = [10, 100, 500, 1000]

SET_STRING_LENGTH : int = 10
MIN_STRING_LENGTH : int = 10
MAX_STRING_LENGTH : int = 20

AMT_SWAPPED_PAIRS : int = 5

AMT_REPEATS       : int = 10

UNIT_NAME         : str = "secs"
UNIT_FACTOR       : float = 1

#initialisation
trees = {
    "TWO_THREE_TREE" : TWO_THREE(),
    "LLRB_TREE" : LLRBBST()
}

#data generation
def generateDataset(func : function, strLen : int, maxStrLen : int = 0, amtSwappedPairs : int = 0) -> list[list[str]]:
    if amtSwappedPairs:
        return [func(DATASET_SIZE, strLen, maxStrLen, amtSwappedPairs) for DATASET_SIZE in DATASET_SIZES] 
    return [func(DATASET_SIZE, strLen, maxStrLen) for DATASET_SIZE in DATASET_SIZES] 

#separate datasets
datasets : dict[str, list[list[str]]] = dict()

datasets["set_random"]          = generateDataset(genRandList, SET_STRING_LENGTH)
datasets["set_sorted"]          = generateDataset(genSortedList, SET_STRING_LENGTH)
datasets["set_nearly_sorted"]   = generateDataset(genNearlySortedList, SET_STRING_LENGTH, amtSwappedPairs=AMT_SWAPPED_PAIRS)

datasets["range_random"]        = generateDataset(genRandList, MIN_STRING_LENGTH, MAX_STRING_LENGTH)
datasets["range_sorted"]        = generateDataset(genSortedList, MIN_STRING_LENGTH, MAX_STRING_LENGTH)
datasets["range_nearly_sorted"] = generateDataset(genNearlySortedList, MIN_STRING_LENGTH, MAX_STRING_LENGTH, AMT_SWAPPED_PAIRS)

#test
#dict[treeName : str, dict[datasetName : str, list[seconds : int]]]
putDatasetsTimes : dict[str, dict[str, list[int]]] = dict()
getDatasetsTimes : dict[str, dict[str, list[int]]] = dict()

methodDatasetTimes = {"put" : putDatasetsTimes, "get" : getDatasetsTimes}

def gatherTimes(savedDict : dict[str, dict[str, list[int]]], methodName : str, datasets, trees):
    for treeName, tree in trees.items():
        savedDict[treeName] = dict()
        for datasetName, dataset in datasets.items():
            times : list[int] = list()
            for data in dataset:
                for element in data:
                    times.append(timeit(lambda : getattr(tree, methodName)(element), number = AMT_REPEATS))
                savedDict[treeName][datasetName] = times

for methodName, datasetTimes in methodDatasetTimes.items():
    gatherTimes(datasetTimes, methodName, datasets, trees)

#show stats
for treeName in trees.keys():
    print(f"{treeName}:")
    print()
    print(f"{AMT_REPEATS}\tREPEAT COUNTS")
    print(f"{SET_STRING_LENGTH}\tFIXED STRING LENGTH")
    print(f"[{MIN_STRING_LENGTH}-{MAX_STRING_LENGTH}]\tMIXED STRING LENGTH RANGE")
    print(f"{AMT_SWAPPED_PAIRS}\tNEARLY SORTED DISTURBED PAIRS AMOUNT")
    print()
    for datasetName in datasets.keys():
        print(f"\t{datasetName}:")
        for methodName, datasetTimes in methodDatasetTimes.items():
            print(f"\t\t{methodName}:")

            total = sum(datasetTimes[treeName][datasetName])
            totalSquares = sum(map(lambda time : time**2, datasetTimes[treeName][datasetName]))
            num = len(datasetTimes[treeName][datasetName])

            average = total/num
            averageSquares = totalSquares/num

            stddev = (averageSquares - (average**2))**0.5

            print(f"\t\t\tAVERAGE:\t{average*UNIT_FACTOR}\t{UNIT_NAME}")
            print(f"\t\t\tSTD.DEV:\t{stddev*UNIT_FACTOR}\t{UNIT_NAME}")




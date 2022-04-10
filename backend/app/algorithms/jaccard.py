from utils import union, intersection

def computeJaccardIndex(setA, setB):
    """
    The Jaccard Index, also known as the Jaccard similarity coefficient,
    is a statistic used in understanding the similarities between 
    sample sets. 
    The measurement emphasizes similarity between finite sample sets, 
    and is formally defined as the size of the intersection divided 
    by the size of the union of the sample sets.
    """
    return  len(intersection(setA, setB)) / len(union(setA, setB))

def computeJaccardDistance(setA, setB):
    return 1 - computeJaccardIndex
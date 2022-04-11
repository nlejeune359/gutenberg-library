import networkx as nkx
from algorithms.jaccard import createJaccardGraph


def rankBooks(books):
    G = createJaccardGraph(books)
    resDict = nkx.closeness_centrality(G, distance='weight')

    return resDict


def sortSearchResponse(searchRes):
    books = set(map(lambda x: x["id"], searchRes))

    IDDict = rankBooks(books)

    for item in searchRes:
        item["centrality"] = IDDict[item["id"]]

    searchRes.sort(key=lambda x: x["centrality"], reverse=True)
    return searchRes

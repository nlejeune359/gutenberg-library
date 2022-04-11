from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, ConsultedBooks, Tags, Tagmaps, Users, Subjects, SubjectMaps
from utils import union, intersection, db_string, JACCARD_INDEX_EDGE
import networkx as nx


def computeJaccardIndex(setA, setB):
    """
    The Jaccard Index, also known as the Jaccard similarity coefficient,
    is a statistic used in understanding the similarities between
    sample sets.
    The measurement emphasizes similarity between finite sample sets,
    and is formally defined as the size of the intersection divided
    by the size of the union of the sample sets.
    """
    return len(intersection(setA, setB)) / len(union(setA, setB))


def computeJaccardDistance(setA, setB):
    return 1 - computeJaccardIndex


def createJaccardGraph(booksIDList):
    db_sal = create_engine(db_string)
    Session = sessionmaker(db_sal)
    session = Session()

    subjectMapsFromDB = session.query(SubjectMaps.book_id, SubjectMaps.subject_id).filter(SubjectMaps.book_id.in_(booksIDList)).all()

    dictBook = {}

    for sub in subjectMapsFromDB:
        if sub.book_id in dictBook:
            dictBook[sub.book_id].append(sub.subject_id)
        else:
            dictBook[sub.book_id] = [sub.subject_id]

    # Create all nodes
    G = nx.Graph()
    G.add_nodes_from(booksIDList)

    # Create edge
    alreadyTreated = []
    for nodeA in dictBook:
        if nodeA not in alreadyTreated:
            for nodeB in dictBook:
                if nodeA != nodeB:
                    jacIndex = computeJaccardIndex(dictBook[nodeA], dictBook[nodeB])
                    if jacIndex >= JACCARD_INDEX_EDGE:
                        G.add_edge(nodeA, nodeB, weight=jacIndex)
        alreadyTreated.append(nodeA)

    return G

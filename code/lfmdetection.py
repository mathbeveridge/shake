#networkx is required to compile
import networkx as nx
import matplotlib.pyplot as plt

import random
import community
import csv


#################################
#
# Detecting overlapping and hierarchical community structure in complex networks
# Based on Lancichinetti , Fortunato and Kertesz
#
# Coded by Haihan Lin

def calculateFitness (subgraphG):
    internalDegree = 0
    subgraphEdgelist = subgraphG.edges(data= "weight")
    for e in subgraphEdgelist:
        internalDegree += 2*e[2]
    externalDegree = 0
    tempList = G.edges(subgraphG.nodes(),data = 'weight')
    externalEdgeList = [x for x in tempList if x not in subgraphEdgelist]
    for e in externalEdgeList:
        externalDegree += e[2]
    if internalDegree + externalDegree == 0:
        return 0
    return (internalDegree)/pow((internalDegree+externalDegree),alpha)

def calculateNodeFitness (subgraphG, nodeA):
    #print("SG nodes", list(subgraphG.nodes()), nodeA)
    subgraphGWithA = G.subgraph(list(subgraphG.nodes())+[nodeA])
    fitnessWithA = calculateFitness(subgraphGWithA)
    fitnessWithoutA = calculateFitness(subgraphG)
    return fitnessWithA - fitnessWithoutA

def detectNaturalCommunity(nodeA):
    currentCommunity = G.subgraph(nodeA)
    while(True):
        nodeAdded = False
        currentLargestFitness = 0
        for v in G.nodes():
            if v not in currentCommunity.nodes():
                fitness = calculateNodeFitness(currentCommunity,v)
                if fitness>currentLargestFitness:
                    nodeAdded = True
                    currentLargestNeighbor = v
                    currentLargestFitness = fitness

        if not nodeAdded:
            break
        else:
            currentCommunity = G.subgraph(list(currentCommunity.nodes())+[currentLargestNeighbor])
            removed = True
            while(removed):
               newCommunity = currentCommunity
               removed = False
               for n in currentCommunity.nodes():
                   if (calculateNodeFitness(currentCommunity,n)<0):
                        newCommunity = G.subgraph(newCommunity.nodes().remove(n))
                        removed = True
               currentCommunity = newCommunity
    return currentCommunity

def detectAllCommunities(iterationThreshold):
    communityCount = 1
    notCounted = range(len(G.nodes()))
    communities = []
    while (communityCount==1):

        communities = []
        iterationTimes = 0
        while(len(notCounted)>0 and iterationTimes<iterationThreshold):
            n = notCounted[random.randrange(len(notCounted))]
            newCommunity = detectNaturalCommunity(n)
            if (len(newCommunity.nodes())!=len(G.nodes()) & iterationTimes<iterationThreshold):
                communities.append(newCommunity)
                notCounted = [x for x in notCounted if x not in newCommunity.nodes()]
            else:
                iterationTimes +=1

        communityCount = len(communities)
    return [x for x in communities if (len(x) != 1 and len(x)!=len(G.nodes()))]

def runrun(alVal, time, iterationThreshold):
    print("")
    alpha = alVal
    j=0
    communities = detectAllCommunities(iterationThreshold)
    communityCount = len(communities)
    print("found communities=", communityCount)

    dictionaryT = idToLabel.copy()
    for key in dictionaryT.keys():
        dictionaryT[key] = []
    for i in communities:
        print("Community",j)
        print(len(i.nodes()))
        #print(i.nodes())
        final = "["
        for v in i.nodes():

            final += (idToLabel[v] + ", ")
        print(final + "]")

        for v in i.nodes():
            #lab = idToLabel[v]
            dictionaryT[v] += [j]
        j += 1

    filename = "dolphin" + str(time) +"Alpha" +str(alpha)+ ".csv"
    myfile = open(filename, 'w')
    wr = csv.writer(myfile,quoting = csv.QUOTE_NONE)
    firstRow = ["ID", "Label"]

    for i in range(communityCount):
        firstRow+=["Com"+str(i+1)]
    wr.writerow(firstRow)
    overLaps = ""
    for key in dictionaryT:
        valueList = dictionaryT[key]
        resultString = [key,key]
        if len(valueList)>=2:
            overLaps += (str(key)+", ")
        for i in range(communityCount):
            if i in valueList:
                resultString+=[str(1)]
            else:
                resultString+=[str(0)]
        wr.writerow(resultString)
    if (len(overLaps)!=0):
        print("Overlaps: ", overLaps)


def modularityTest():
    part = community.best_partition(G)
    communityIndex = 0
    partitionList = {}
    while (True):

        changed = False
        list = []
        for k,v in part.items():
            if v==communityIndex:
                changed = True
                list += [idToLabel[k] + ", "]
        if (not changed):
            break
        print("mod", communityIndex)
        print(list)
        communityIndex+=1


##########################################
#Fill in file path for the network. Assuming it is an edge CSV file


G = nx.Graph()
lines = open("/Users/abeverid/PycharmProjects/shake/out/macbeth-bak/macbethedge-nx.csv", 'r').readlines()
G1 = nx.parse_edgelist(lines, nodetype = str, delimiter=",", data=[("weight", int)])
G1.edges(data=True)
print("G is ", G1)
labelToId = {}
idToLabel = {}
id = 0
print(len(G1.edges()))
for v in G1.nodes():
    labelToId[v] = id
    idToLabel[id] = v
    G.add_node(id)
    id+=1
for e in G1.edges(data = "weight"):
    v1 = e[0]
    v2 = e[1]
    id1 = labelToId[v1]
    id2 = labelToId[v2]
    G.add_edge(id1,id2, weight = e[2])

alpha = 1.5

print("G edges are ", G.edges())

#runrun(1.2, 1, 3)
communities = detectAllCommunities(120)


j=0

for i in communities:
    print("Community", j, "size=", len(i.nodes()))
    # print(i.nodes())
    final = "["
    for v in i.nodes():
        final += (idToLabel[v] + ", ")
    print(final + "]")
    j += 1

#print("all done")

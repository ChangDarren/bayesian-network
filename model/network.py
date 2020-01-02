from model.node import Node

class Network:
    def __init__(self, possibleValues, parents, CPTs):
        """
            parents - dictionary mapping each variable to its direct parents

            CPTs - list of dictionary mapping the current 
            variable name to another dictionary mapping the dependencies 
            value to a prob.

            e.g. 'Result' : {
                'Result = good | Intelligence = high, hasHelp = True': 0.5, 
                ...
            }

            possibleValues - dictionary of variables mapped to their
            possible values
        """
        self.possibleValues = possibleValues

        # Build up the adjacency list
        self.adjList = []
        self.nodes = dict()
        self.nodeToIndex = dict()
        self.indexToNode = dict()

        for index, cpt in enumerate(CPTs):
            key = list(cpt.keys())[0]
            # adjList[index] contains the nodes that this node maps to
            self.adjList.append(list())
            self.nodeToIndex[key] = index
            self.indexToNode[index] = key 

            currVals = dict()
            # Map the variable to an index
            currVals[key] = possibleValues[key]

            parent = parents[key]
            parentVals = dict()
            for p in parent:
                parentVals[p] = possibleValues[p]
            newNode = Node(index, currVals, parentVals)
            newNode.fillTable(cpt[key])
            self.nodes[key] = newNode

        # Fill up the adjacency list
        for index, cpt in enumerate(CPTs):
            varName = list(cpt.keys())[0]
            parent = parents[varName]
            for p in parent:
                pIndex = self.nodeToIndex[p]
                self.adjList[pIndex].append(index)

    def topoSort(self):
        """
            Returns the variables in topological sorted order
        """
        track = dict()
        done = dict()
        sortedList = []
        for node in self.nodes:
            index = self.nodeToIndex[node]
            track[index] = 0

        for toList in self.adjList:
            for indexTo in toList:
                track[indexTo] += 1

        while len(sortedList) < len(self.nodes):
            for index in self.indexToNode:
                if track[index] == 0 and index not in done:
                    sortedList.append(self.indexToNode[index])
                    done[index] = 1
                    for to in self.adjList[index]:
                        track[to] -= 1

        return sortedList
    
    def getFactors(self, conditions):
        """
            conditions - dictionary mapping variables to their fixed value
        """
        factors = []
        for var in self.nodes:
            factors.append(self.nodes[var].getFactor(conditions))

        return factors
    

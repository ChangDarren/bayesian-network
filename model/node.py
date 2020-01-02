from model.table import Table

class Node:
    def __init__(self, id, variable, dependencies):
        """
            variable - dictionary containing the variable name to its
            possible values

            dependencies - dictionary containing the dependencies to its
            possible values
        """
        self.id = id
        self.varName = list(variable.keys())[0]
        self.table = Table(variable, dependencies)

    def getVarName(self):
        return self.var_name

    def fillTable(self, cptMapping):
        """
            cptMapping - dictionary mapping the probability query to
            the probability value
        """
        for mapping in cptMapping:
            query, evidence = self._unpackMap(mapping)
            self.setProb(query, evidence, cptMapping[mapping])

    def _unpackMap(self, mapping):
        """
            mapping - string of the form of a probability query
            e.g. A = True | B = False,
                 A = False
            
            Returns:
                query - dictionary mapping the variable and its value
                evidence - dictionary mapping the evidence and its value
        """
        if mapping.find('|') != -1:
            queryStr, evidenceStr = mapping.split('|')
        
            query = dict()
            queryVar, queryVal = [x.strip() for x in queryStr.split('=')]
            query[queryVar] = queryVal

            evidence = dict()
            eviStrs = [x.strip() for x in evidenceStr.split(',')]
            for eviStr in eviStrs:
               eviVar, eviVal = [x.strip() for x in eviStr.split('=')]
               evidence[eviVar] = eviVal

            return (query, evidence)
        else:
            query = dict()
            queryVar, queryVal = [x.strip() for x in mapping.split('=')]
            query[queryVar] = queryVal

            return (query, None)

    def getProb(self, query, evidence):
        return self.table.getProb(query, evidence)

    def setProb(self, query, evidence, prob):
        self.table.setProb(query, evidence, prob)

    def getFactor(self, conditions):
        return self.table.getFactor(conditions)

if __name__ == '__main__':
    id = 1
    variable = { 'Grade' : ['A', 'B', 'C'] }
    dependencies = { 
        'Difficulty': ['high', 'low'], 
        'Intelligence': ['high', 'low'] 
    }

    cptMapping = {
        'Grade = A | Difficulty = high, Intelligence = high': 0.5,         
        'Grade = A | Difficulty = high, Intelligence = low': 0.05,         
        'Grade = A | Difficulty = low, Intelligence = high': 0.9,         
        'Grade = A | Difficulty = low, Intelligence = low': 0.3,         
        'Grade = B | Difficulty = high, Intelligence = high': 0.3,         
        'Grade = B | Difficulty = high, Intelligence = low': 0.25,         
        'Grade = B | Difficulty = low, Intelligence = high': 0.08,         
        'Grade = B | Difficulty = low, Intelligence = low': 0.4,         
        'Grade = C | Difficulty = high, Intelligence = high': 0.2,         
        'Grade = C | Difficulty = high, Intelligence = low': 0.7,         
        'Grade = C | Difficulty = low, Intelligence = high': 0.02,         
        'Grade = C | Difficulty = low, Intelligence = low': 0.3,         
    }
    
    node_1 = Node(id, variable, dependencies) 
    node_1.fillTable(cptMapping)

    factor_1 = node_1.getFactor()

    varKey, varVal = list(dependencies.items())[0]
    elimVar = { varKey: varVal }
    factor_1.sum(elimVar)

    id = 2
    variable = { 'A': ['high', 'mid', 'low'] }
    dependencies = { 'B': ['T', 'F'] }
    cptMapping = {
        'A = high | B = T': 0.5, 
        'A = high | B = F': 0.8, 
        'A = mid | B = T': 0.1, 
        'A = mid | B = F': 0.0, 
        'A = low | B = T': 0.3, 
        'A = low | B = F': 0.9, 
    }

    node_2 = Node(id, variable, dependencies)
    node_2.fillTable(cptMapping)
    factor_2 = node_2.getFactor()

    id = 3
    variable = { 'B': ['T', 'F'] }
    dependencies = { 'C': ['T', 'F'] }
    cptMapping = { 
        'B = T | C = T': 0.5,
        'B = T | C = F': 0.7,
        'B = F | C = T': 0.1,
        'B = F | C = F': 0.2,
    }
    node_3 = Node(id, variable, dependencies)
    node_3.fillTable(cptMapping)
    factor_3 = node_3.getFactor()

    factor_4 = factor_2.product(factor_3)
    print(factor_4)


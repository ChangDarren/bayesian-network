import copy

class Factor:
    def __init__(self, factors, table):
        """
            factors - list of variables that this factor is dependent on
            table - dictionary mapping the values of the variables to 
            the probability value
            The order of the values in the tuple should be in the same
            order as the variable in factors.
        """
        self.factors = factors
        self.table = table

    def sum(self, var):
        """
            var - dictionary mapping the variable name to list of possible values
        """
        varName = list(var.keys())[0]
        possibleVals = var[varName]

        # Get index of the var according to factors
        for index, factor in enumerate(self.factors):
            if factor == varName:
                factorIndex = index
        newFactors = self.factors[:factorIndex] + self.factors[factorIndex + 1:]
        
        newTable = dict()
        for key in self.table:
            newKey = key[:factorIndex] + key[factorIndex + 1:]
            if newKey not in newTable:
                newTable[newKey] = self.table[key]
            else:
                newTable[newKey] += self.table[key]

        self.factors = newFactors
        self.table = newTable

    def product(self, otherFactor):
        factor_1 = set(self.factors)
        factor_2 = set(otherFactor.factors)

        intersect = factor_1.intersection(factor_2)
        
        # Get the index of those that are intersected
        intersect_factor_1 = []
        intersect_factor_2 = []
        for var in intersect:
            index = self.factors.index(var)
            intersect_factor_1.append(index)

            index = otherFactor.factors.index(var)
            intersect_factor_2.append(index)

        newFactors = copy.copy(self.factors)
        newTable = dict()

        for var in otherFactor.factors:
            if var not in intersect:
                newFactors.append(var)

        for entry_1 in self.table:
            for entry_2 in otherFactor.table:
                # Check those that intersect matches in value
                canMerge = True
                for i in range(len(intersect_factor_1)):
                    if entry_1[intersect_factor_1[i]] != entry_2[intersect_factor_2[i]]:
                        # print(entry_1[i], entry_2[i])
                        canMerge = False

                if canMerge:
                    new_entry = copy.copy(entry_1)
                    # Go through the entry and take only those that are not in the
                    # intersection

                    for index, val in enumerate(entry_2):
                        if index not in intersect_factor_2:
                            new_entry += (val, )
                    
                    newTable[new_entry] = self.table[entry_1] * otherFactor.table[entry_2]

        return Factor(newFactors, newTable)


    def __str__(self):
        output = 'factors: ' + str(self.factors) + '\n'
        for entry in self.table:
            output += str(entry) + ': ' + str(self.table[entry]) + '\n'

        return output


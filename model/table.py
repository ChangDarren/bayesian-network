import itertools
import copy

from model.factor import Factor

class Table:
    def __init__(self, variable, dependencies):
        """
            variable - dictionary of variable and its possible values
            dependencies - dictionary of dependencies, with the possible values

            Standardise and always put the variable first
        """
        self.varName = list(variable.keys())[0]
        self.dependencies = sorted(list(dependencies.keys()))
        self.factors = [self.varName]
        self.factors += self.dependencies
        values = [variable[self.varName]]

        for dependencyVal in self._unpackDependencies(dependencies):
            values.append(dependencyVal)

        self.table = dict()
        for key in itertools.product(*values):
            self.table[key] = None

    def _unpackDependencies(self, dependencies):
        """
            Helper function to unpack the values of the dependencies
            base on the alphabetical order of the key
        """
        
        if not dependencies:
            return []

        vals = []
        for key in sorted(dependencies.keys()):
            vals.append(dependencies[key])
        return vals

    def getFactor(self, conditions):
        newTable = dict(self.table)
        for var in conditions:
            # We need to fix the entry for the var in this factors
            if var in self.factors:
                loc = self.factors.index(var)
                newTable = {key: newTable[key] for key in newTable if key[loc] == conditions[var]}
        
        return Factor(self.factors, newTable)

    def setProb(self, query, evidence, prob):
        """
            query - dictionary of variable with its value
            evidence - dictionary of value of dependencies
        """
        
        # Check that the dependencies match
        assert (not evidence) or self.dependencies == sorted(list(evidence.keys()))
        assert self.varName in query

        entry = (query[self.varName], )
        for val in self._unpackDependencies(evidence):
            entry += (val, )
        
        # The entry should be legal
        assert entry in self.table
        self.table[entry] = prob

    def getProb(self, query, evidence):
        """
            query - dictionary of variable with its value
            evidence - dictionary of value of dependencies
        """

        # Check that the dependencies match
        assert self.dependencies == sorted(list(evidence.keys()))
        assert self.varName in query

        entry = (query[self.varName], )
        for val in self._unpackDependencies(evidence):
            entry += (val, )
        
        # The entry should be legal
        assert entry in self.table
        return self.table[entry]

    def __str__(self):
        output = ''
        for entry in self.table:
            # if self.table[entry]:
            output += str(entry) + ': ' + str(self.table[entry]) + '\n'

        return output

if __name__ == '__main__':
    dependencies = { 'Intelligence': ['high', 'mid', 'low'], 'hasHelp': ['True', 'False']}
    currVar = { 'Result': ['good', 'bad'] }
    table = Table(currVar, dependencies)
    table.setProb({ 'Result': 'good' }, { 'hasHelp': 'True', 'Intelligence': 'high' }, 0.5)
    print(table.getProb({ 'Result': 'good' }, { 'hasHelp': 'True', 'Intelligence': 'high' }))

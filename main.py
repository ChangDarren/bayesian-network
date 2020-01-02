from model.network import Network
from ve import sum_product_ve

if __name__ == '__main__':
    possibleValues =  { 
        'A': ['T', 'F'], 
        'B': ['T', 'F'], 
        'C': ['T', 'F'], 
        'D': ['T', 'F'], 
        'E': ['T', 'F']
    }

    parents = {
        'A': [], 
        'B': [], 
        'C': ['A'], 
        'D': ['A', 'B'], 
        'E': ['C']
    }

    CPTs = [
        { 
            'A': { 
                'A = T': 0.3, 
                'A = F': 0.7
            }
        }, 
        {
            'B': {
                'B = T': 0.6, 
                'B = F': 0.4
            }    
        }, 
        {
            'C': {
                'C = T | A = T': 0.8, 
                'C = F | A = T': 0.2, 
                'C = T | A = F': 0.4, 
                'C = F | A = F': 0.6
            }
        }, 
        {
            'D': {
                'D = T | A = T, B = T': 0.7,
                'D = F | A = T, B = T': 0.3,
                'D = T | A = T, B = F': 0.8,
                'D = F | A = T, B = F': 0.2,
                'D = T | A = F, B = T': 0.1,
                'D = F | A = F, B = T': 0.9,
                'D = T | A = F, B = F': 0.2,
                'D = F | A = F, B = F': 0.8,
            }
        }, 
        {
            'E': {
                'E = T | C = T': 0.7, 
                'E = F | C = T': 0.3, 
                'E = T | C = F': 0.2, 
                'E = F | C = F': 0.8
            }
        }
    ]

    conditions = { 
        'D' : 'F', 
        'C' : 'T'
    }

    net = Network(possibleValues, parents, CPTs)
    factors = net.getFactors(conditions)
    order = net.topoSort()

    ans = sum_product_ve(factors, order, possibleValues)
    print(ans)

def sum_product_ve(factors, vars, possibleValues):
    for var in vars:
        factors = sum_product_elim(factors, var, possibleValues)

        ans = factors[0]
        for index, factor in enumerate(factors):
            if index == 0:
                continue

            ans = ans.product(factor)

    return ans

def sum_product_elim(factors, elim_var, possibleValues):
    """
        factors - list of factors
        elim_var - dictionary mapping the variable name to the 
        possible values
    """
    subset = []
    new_set = []
    for factor in factors:
        if elim_var in factor.factors:
            subset.append(factor)
        else:
            new_set.append(factor)

    newFactor = subset[0]

    for index, factor in enumerate(subset):
        if index == 0:
            continue

        newFactor = newFactor.product(factor)
    
    elim_var_val = { elim_var: possibleValues[elim_var] }
    newFactor.sum(elim_var_val)
    new_set.append(newFactor)

    # for factor in new_set:
    #     print(factor)
    # print('-'*20)

    return new_set


'''
Module with utility functions used in more than one module.
'''

import Data
import math
import random


'''
Computes the entropy of a partition.
Receives a dictionary with the proportions of each class.
partitions is the proportion of elements in each class (is a list).
Returns the entropy of such a partition.
'''


def __entropy(partitions):
    __entropy = 0
    for key in partitions:
        if partitions[key] > 0:
            __entropy -= partitions[key]*math.log2(partitions[key])
        elif partitions[key] < 0:
            return "Utils.__entropy: numbers in partitions must be non-negative"
    return __entropy


'''
Compute the profit of splting the trainning set data across the attribute
corresponding to the index i.
data is a list of instances. Each instance is another list.
index is a non-negative number representing the attribute (the index
in the instance list).
values is a list with two different meanings:
    if len(values) == 1: the value in values represent a cutting point for a
    numerical attribute
    elif len(values) > 1: the values in values represent the discrete values
    for the attribute
classes is a list with all the possible class values.
Returns the information profit of such a partiton.
'''


def profit(data, index, values, classes):
    # For computing the proportions of each class inside data
    proportions_of_data = {}

    # In the if case we use this function to find the optimum splitting point
    # for a numberical or continuous attribute (turning it into a discrete
    # attribute).
    if len(values) == 1:
        # count the number of instances with attribute value
        # less or equal than values[0]
        less = 0
        # dictionaries with the proportions of each class inside the instances
        # with attribute value <= than values[0] and > than values[0]
        # (one dictionary for each group).
        proportions_of_less = {}
        proportions_of_greater = {}
        for c in classes:
            proportions_of_less[c] = 0.0
            proportions_of_greater[c] = 0.0
            proportions_of_data[c] = 0.0

        for instance in data:
            proportions_of_data[instance[-1]] += 1
            if instance[index] <= values[0]:
                less += 1
                proportions_of_less[instance[-1]] += 1
            else:
                proportions_of_greater[instance[-1]] += 1

        # divide the amount of instances of each class by the number of
        # instances to get the proportions
        if less > 0:
            for key in proportions_of_less:
                proportions_of_less[key] /= less
        if less != len(data):
            for key in proportions_of_greater:
                proportions_of_greater[key] /= len(data) - less
        for key in proportions_of_data:
            proportions_of_data[key] /= len(data)

        # For debugging
        '''
        print("less={num_less}".format(num_less=less))
        print("proportions_of_data = {proportion}".format(
            proportion=proportions_of_data))
        print("proportions_of_less = {proportion}".format(
            proportion=proportions_of_less))
        print("proportions_of_greater = {proportion}".format(
            proportion=proportions_of_greater))
        '''

        # Return information gain
        return (__entropy(proportions_of_data) -
                less/len(data) * __entropy(proportions_of_less) -
                (len(data) - less)/len(data) * __entropy(proportions_of_greater))

    # In the elif case, we are dealing with discrete attributes.
    elif len(values) > 1:
        # dictionary with dictionaries of proportions of classes for instances
        # with each possible value of the attribute
        list_of_proportions = {}
        # compute the number of instances with each of the possible values
        instances_per_value = {}
        for value in values:
            instances_per_value[value] = 0
            list_of_proportions[value] = {}
            for c in classes:
                list_of_proportions[value][c] = 0.0

        # compute the proportion of each class inside data
        proportions_of_data = {}
        for c in classes:
            proportions_of_data[c] = 0.0

        for instance in data:
            instances_per_value[instance[index]] += 1
            proportions_of_data[instance[-1]] += 1
            list_of_proportions[instance[index]][instance[-1]] += 1

        # divide the amount of instances of each class by the number of
        # instances to get proportions
        for c in classes:
            proportions_of_data[c] /= len(data)
            for value in values:
                if instances_per_value[value] > 0:
                    list_of_proportions[value][c] /= instances_per_value[value]

        # return the information gain
        profit = __entropy(proportions_of_data)

        # For debugging
        '''
        print("proportions_of_data = {proportion}".format(
            proportion=proportions_of_data))
        print("list_of_proportions = {proportion}".format(
            proportion=list_of_proportions))
        print("instances_per_value = {proportion}".format(
            proportion=instances_per_value))
        print("profit = {profit}".format(profit=profit))
        '''

        for value in values:
            profit -= (instances_per_value[value]/len(data) *
                       __entropy(list_of_proportions[value]))
        return profit
    else:
        return "Utils.profit: values must be non-empty"


def weighted_random(values, distribution):
    rand_num = random.random()
    cumulative_distribution = 0
    for i in range(len(distribution)):
        cumulative_distribution += distribution[i]
        if rand_num < cumulative_distribution:
            return values[i]
        

if __name__ == '__main__':
    assert __entropy({1: 0.5, 2: 0.5}) == 1
    assert __entropy({1: 1.0, 2: 0.0}) == 0
    data1 = [
        [1, 1, 1, 0],
        [2, 1, 1, 1],
        [1, 1, 1, 0],
        [2, 1, 1, 1],
        [1, 1, 1, 0],
        [2, 1, 1, 1],
        [1, 1, 1, 0],
        [2, 1, 1, 1]
    ]
    index1 = 0
    values1 = [1]
    classes1 = [0, 1]
    assert profit(data1, index1, values1, classes1) == 1
    data2 = [
        [1, 1, 1, 0],
        [2, 1, 1, 1],
        [3, 1, 1, 2],
        [1, 1, 1, 0],
        [2, 1, 1, 1],
        [3, 1, 1, 2],
        [1, 1, 1, 0],
        [2, 1, 1, 1],
        [3, 1, 1, 2]
    ]
    index2 = 0
    values2 = [1, 2, 3, 4]
    classes2 = [0, 1, 2, 3, 4, 5]
    assert profit(data2, index2, values2, classes2) + math.log2(1/3) < 0.00001

    print(weighted_random([1,2,3], [0.1,0.8,0.1]))
    print(weighted_random([1,2,3], [0.1,0.8,0.1]))
    print(weighted_random([1,2,3], [0.1,0.8,0.1]))

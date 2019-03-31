'''
Module with utility functions used in more than one module.
'''

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
            return(
                "Utils.__entropy: numbers in partitions must be non-negative")
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

        # Return information gain
        return (__entropy(proportions_of_data) -
                less/len(data) * __entropy(proportions_of_less) -
                (len(data) - less)/len(data) *
                __entropy(proportions_of_greater))

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

        for value in values:
            profit -= (instances_per_value[value]/len(data) *
                       __entropy(list_of_proportions[value]))
        return profit
    else:
        return "Utils.profit: values must be non-empty"


'''
Given a list of values and a list of distributions for each of them,
returns a randomly selected value following the distribution.
'''


def weighted_random(values, distribution):
    rand_num = random.random()
    cumulative_distribution = 0
    for i in distribution.keys():
        cumulative_distribution += distribution[i]
        if rand_num < cumulative_distribution:
            return i

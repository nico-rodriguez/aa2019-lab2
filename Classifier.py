'''
Classifier module implementation

This module's responsibility is to classify a preprocessed data set using n
ID3 decsion trees.
'''

import ID3
import Data
import Evaluator
import random
import re


# devides data.dataset into two data sets, the first which is
# k-1 pieces and the latter which consists of only one piece.
# returns the lists of pairs (training, validation) subsets
def k_fold_cross_validation(data, k):
    k_partition_len = len(data.dataset)/k
    dataset_aux = data.dataset.copy()
    dataset_training_aux = data.dataset.copy()
    k_division_list = []
    aux_list = []
    result_list = []
    # the k partitions are cerated to ensure no element is used more than once
    # in each of the iterations
    for i in range(0, k):
        for i in range(0, k_partition_len):
            data_index = random.randint(0, len(dataset_aux))
            aux_list.append(dataset_aux[data_index])
            del dataset_aux[data_index] # we remove it to avoid duplicates
            del dataset_training_aux[data_index] # an element in the validation set isnt in the 
                                                 # training set for this iteration
        k_division_list.append(aux_list)
        # the k division list is used as this iterations validation set
        result_list.append((dataset_training_aux, aux_list.copy()))
        # reset relevant structures
        dataset_training_aux = data.dataset.copy()
        aux_list = []
        k_division_list = []
    return result_list


# creates both validation and training sets from data
def divide_corpus(data, percetnage_training):
    validation_set = data.dataset.copy()
    training_set = []
    partition_length = round(len(data.dataset) * percetnage_training)
    for i in partition_length:
        data_index = random.randint(0, len(validation_set))
        training_set.append(validation_set[data_index])
        # data thats on training set cant be on validation set
        del validation_set[data_index]  
    return (training_set, validation_set)


# returns the class of the instance according to tree
def classify(tree, instance):
    # first node is fetched by hand
    current_path = "Attribute None = None"
    current_node = tree.get_node(current_path)
    # while we havent hit a leave
    while "Class" not in current_node.tag:
        # node tags are in the form "attribute x" where x is its id which is fecthed
        # a simple regex
        current_attribute = int(re.findall(r'\d+', current_node.tag)[0])
        attribute_value = instance[current_attribute]
        # continue to move inside tree with the transition
        target_id = (current_path + ",Attribute " + str(current_attribute) +
                     " = " + str(attribute_value) + ",")
        current_node.get_node(target_id)
    return current_node.tag


if __name__ == "__main__":
    data = Data.Data('iris')
    divided_corpus = divide_corpus(data, 0.80)
    iris_tree = ID3(divided_corpus[0])
    list_of_classified_instances = []
    for instance in divided_corpus[1]:
        list_of_classified_instances.append((
            classify(iris_tree, instance), instance))
    print(list_of_classified_instances)

'''
Classifier module implementation

This module's responsibility is to classify a preprocessed data set using n
ID3 decsion trees.
'''

import ID3
import Data
import Evaluator
import Utils
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


# returns the class of the instance according to tree
def classify(tree, instance, distribution):
    # first node is fetched by hand
    print(instance)
    current_path = "Attribute None = None,"
    current_node = tree.get_node(current_path)
    # while we havent hit a leave
    while "Class" not in current_node.tag:
        # node tags are in the form "attribute x" where x is its id which is 
        # fecthed a simple regex
        current_attribute = int(re.findall(r'\d+', current_node.tag)[0])
        attribute_value = instance[current_attribute]
        # continue to move inside tree with the transition
        current_path = (current_path + "Attribute " + str(current_attribute) +
                        " = " + str(attribute_value) + ",")
        print(current_path)
        current_node = tree.get_node(current_path)
        if current_node is None:
            random_class = Utils.weighted_random(
                list(distribution.keys()), list(distribution.values()))
            return ("Class " + str(random_class) + " Instances "
                    + str(distribution[random_class]))
    return current_node.tag


if __name__ == "__main__":
    data = Data.Data('iris')
    divided_corpus = data.divide_corpus(0.80)
    (iris_tree, breakpoints) = ID3.ID3(divided_corpus[0])
    divided_corpus[0].apply_breakpoints(breakpoints)
    divided_corpus[1].apply_breakpoints(breakpoints)
    iris_tree.show(idhidden=False)
    list_of_classified_instances = []
    for instance in divided_corpus[1].dataset:
        list_of_classified_instances.append((
            classify(iris_tree, instance,
                     divided_corpus[0].global_class_distribution),
            instance))
    for instance in list_of_classified_instances:
        print(instance)

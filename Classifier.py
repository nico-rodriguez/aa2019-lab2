'''
Classifier module implementation

This module's responsibility is to classify a preprocessed data set using n
ID3 decsion trees.
'''

import ID3
import Data
import Evaluator
import random


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


if __name__ == "__main__":
    data = Data.Data('iris')
    k_fold_data = k_fold_cross_validation(data, 5)
    iris_trees = []
    iris_results = []
    for partition in k_fold_data:
        iris_trees.append(ID3(Data.Data(partition[0])))
    for i in range(0, len(iris_trees)):
        iris_results.append(Evaluator.evaluate_iris(
            k_fold_data[i][1], iris_trees))

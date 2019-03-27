'''
Classifier module implementation

This module's responsibility is to classify a preprocessed data set using n
ID3 decsion trees.
'''

import ID3
import Data
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
            del dataset_aux[data_index]  # we remove it to avoid duplicates
            # an element in the validation set isnt in the training set for
            # this iteration
            del dataset_training_aux[data_index]
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
        # node tags are in the form "attribute x" where x is its id which
        # is fecthed a simple regex
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


'''
For each element of the dataset, if the element has the label label, it sets
that attribute to 1, otherwise 0 allow new new memory.
'''


def map_dataset(dataset, label):
    new_dataset = dataset.copy()
    for row in new_dataset:
        last_index = len(row)-1
        last_item = row[last_index]
        if last_item == label:
            row[last_index] = (label)
        else:
            row[last_index] = ("NO"+label)
    return new_dataset

# separates


def classify_dataset(data):
    IDtrees = []
    validation_sets = []
    for clss_label in data.classes:
        # Transform the data dataset
        mapped_data = map_dataset(data.dataset, clss_label)
        (training_set, validation_set) = data.divide_corpus(0.8)
        new_data = data.copy()

        # Transform the data metadata
        new_data.dataset = training_set
        new_data.amount_classes = 2
        other_classes_label = "NO"+clss_label
        new_data.classes = [clss_label, other_classes_label]
        distr = 0.0
        for key in data.class_distribution.keys():
            if key != clss_label:
                distr += new_data.class_distribution[key]
        new_data.class_distribution = {clss_label: 1-distr, other_classes_label: distr}
        new_data.global_class_distribution = {
            clss_label: 1-distr, other_classes_label: distr}
        validation_sets.append(validation_set)
        IDtrees.append(ID3(new_data))
    for entry in validation_sets:
        tags = []
        count = 0
        for tree in IDtrees:
            classify_result = classify(tree, entry)
            class_value = int(re.findall(r'Instances \d+', classify_result))
            instances_count = int(re.findall(r'Class \d+', classify_result))
            tags.append([count, class_value, instances_count])
            count += 1


# returns the tag index of which tag of the
# the tree wins (which one is chosen for the input)
def process_tags(tags):

    def filter_func(elem):
        return elem[1] == 1

    def map_func(elem):
        return elem[2]

    def max(a, b):
        if a >= b:
            return a
        else:
            return b

    def isEqual(value, elem):
        return elem[2] == value

    filtered_tags = filter(filter_func, tags)
    mapped_tags = map(map_func, filtered_tags)
    max_val = foldr(max)(tags[0][2])(mapped_tags)
    max_tags = filter((isEqual(max_val)), filtered_tags)
    return (random.sample(max_tags, 1))[0]


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

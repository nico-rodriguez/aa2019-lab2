'''
Classifier module implementation

This module's responsibility is to classify a preprocessed data set using n
ID3 decsion trees.
'''

import copy
import ID3
import Data
import Utils
import random
import re
import os


# Returns the class of the instance according to the tree.
def classify(tree, instance, distribution):
    # first node is fetched by hand
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
        current_node = tree.get_node(current_path)
        if current_node is None:
            random_class = Utils.weighted_random(
                list(distribution.keys()), list(distribution.values()))
            return ("Class " + str(random_class) + ",Instances "
                    + str(distribution[random_class]))
    return current_node.tag


'''
Takes a tree and a set of instances to be evaluated and
returns a list of tuples (true_class, classified_class)
'''


def classify_dataset_tree(tree, data):
    result_list = []
    # classify instances
    for instance in data.dataset:
        result_node_tag = classify(tree, instance,
                                   data.global_class_distribution)
        classified_class = re.findall(r'Class ([^,]+)', result_node_tag)[0]
        true_class = instance[-1]
        result_list.append((true_class, classified_class))
    return result_list


'''
For each element of the dataset, if the element has the label label, it sets
that attribute to 1, otherwise 0, generates new memory for the result.
'''


def map_dataset(dataset, label):
    new_dataset = copy.deepcopy(dataset)
    for row in new_dataset:
        row[-1] = 1 if row[-1] == label else 0
    return new_dataset


'''
Receives a data and classifies the associated dataset using random distribution,
returning a list of pairs [label, guess]
'''

def classify_dataset_random(data):
    result = []
    for elem in data.dataset:
        random_guess = (random.sample(data.classes, 1))
        result.append(elem[-1], random_guess)
    return result

'''
Receives data with 80 percent of the dataset for training.
Returns array with n classification trees where n is the amount of classes.
'''

def generate_forest_classifier(data):
    IDtrees = []
    for class_label in data.classes:
        # Transform the data dataset
        mapped_data = map_dataset(data.dataset, class_label)
        new_data = data.copy()
        new_data.dataset = mapped_data
        # Transform the data metadata
        new_data.amount_classes = 2
        new_data.classes = [1, 0]
        label_distribution = new_data.class_distribution[class_label]
        new_data.class_distribution = {1: label_distribution,
                                       0: 1-label_distribution}
        new_data.global_class_distribution = {1: label_distribution,
                                              0: 1-label_distribution}
        idtree_result = ID3.ID3(new_data)
        IDtrees.append((idtree_result[0], idtree_result[1], new_data.class_distribution))
    return IDtrees


# Classifies a multi-label dataset and returns the generated labels for it
def classify_dataset_multi_label(classifier, data):
    labels = []
    for entry in data.dataset:
        guess = classify_multi_label(classifier, entry)
        guessed_label = data.classes[guess]
        label = entry[-1]
        labels.append([label, guessed_label])
    return labels


# Classifies an entry using the multi-label classifier
def classify_multi_label(classifier, entry):
    tags = []
    count = 0
    for tree in classifier:
        classify_result = classify(tree[0], entry, tree[2])
        instances_count = float(re.findall(r'Instances (\d+\.\d)+',
                                classify_result)[0])
        class_value = int(re.findall(r'Class (\d)+', classify_result)[0])
        tags.append([count, class_value, instances_count])
        count += 1
    guess = tags[process_tags(tags)[0]][0]
    return guess


'''
Returns the tag index of which tag of the
the tree wins (which one is chosen for the input)
'''


def process_tags(tags):

    def filter_func(elem):
        return elem[1] == 1

    def map_func(elem):
        return elem[2]

    def isEqual(value, elem):
        return elem[2] == value

    filtered_tags = list(filter(filter_func, tags))
    if len(filtered_tags) == 0:
        filtered_tags = tags
    mapped_tags = list(map(map_func, filtered_tags))
    max_val = max(mapped_tags)
    max_tags = []
    for elem in filtered_tags:
        if elem[2] == max_val:
            max_tags.append(elem)
    return (random.sample(max_tags, 1))[0]


'''
Receives a classifier's type ("Single" or "Forest"), a training_proportion
(e.g. 0.8), a dataset name ("iris" or "covtype") and a directory path.
Generates the classifier and saves it in the specified directory, toghether
with the training instances and the verification instances split in two files.
'''


def generate_classifier(type, training_proportion, dataset, directory):
    os.mkdir(directory)
    print("Se crea el directorio {dir}".format(dir=directory))

    if dataset == 'iris':
        print('Iris dataset seleccionado')
        data = Data.Data('iris')
        data_training, data_validation = data.divide_corpus(
            training_proportion)

if __name__ == "__main__":
    '''
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
'''
    data = Data.Data('iris')
    (data_training, data_validation) = data.divide_corpus(0.8)
    classifier = generate_forest_classifier(data_training)
    tags = classify_dataset_multi_label(classifier, data_validation)
    print(tags)
'''
Data module

This module's responsibility is to encapsule the parsed data as well as
metadata from the given dataset.
'''
import ast
import random
import Utils
import copy

iris_processed_data = 'processed_data_iris.txt'
covtype_processed_data = 'processed_data_covtype.txt'


class Data:
    '''
    data_name may be 'iris' or 'covtype'.
    parse_dataset_file may be True or False. In the first case, the .data files
    are parsed and converted to Python objects; in the second case, those files
    are not parsed, but the instance_file with the preprocessed instances is
    read instead. The preprocessed instances where converted to Python objects
    with the corresponding types (list, str, int, float, etc...) and the
    numeric attributes where split in two ranges: 0 for those below or equal
    to some cutting point, and 1 for the rest.
    '''
    def __init__(self, data_name):
        self.data_name = data_name
        # Indicates if all instances belong to the same class
        self.monoclass_instances = None
        if data_name == "iris":
            self.amount_attributes = 4
            self.attributes = [0, 1, 2, 3]
            self.attribute_values = {
                0: [0, 1], 1: [0, 1], 2: [0, 1], 3: [0, 1]
            }
            self.amount_classes = 3
            self.classes = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
            self.class_distribution = {
                'Iris-setosa': 1/3, 'Iris-versicolor': 1/3,
                'Iris-virginica': 1/3}
            self.global_class_distribution = {
                'Iris-setosa': 1/3, 'Iris-versicolor': 1/3,
                'Iris-virginica': 1/3}
            with open(iris_processed_data, 'r') as instance_file:
                instances_list = instance_file.readlines()
                self.dataset = []
                for line in instances_list:
                    # Convert the list in the string to a list
                    instance_as_list = ast.literal_eval(line)
                    self.dataset.append(instance_as_list)
        else:
            self.amount_attributes = 12
            self.attributes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            self.attribute_values = {
                0: [0, 1], 1: [0, 1], 2: [0, 1], 3: [0, 1], 4: [0, 1],
                5: [0, 1], 6: [0, 1], 7: [0, 1], 8: [0, 1], 9: [0, 1],
                10: [0, 1, 2, 3], 11: list(range(40))
            }
            self.amount_classes = 7
            self.classes = [0, 1, 2, 3, 4, 5, 6]
            self.class_distribution = {
                0: 211840/581012, 1: 283301/581012, 2: 35754/581012,
                3: 2747/581012, 4: 9493/581012, 5: 17367/581012,
                6: 20510/581012
            }
            self.global_class_distribution = {
                0: 211840/581012, 1: 283301/581012, 2: 35754/581012,
                3: 2747/581012, 4: 9493/581012, 5: 17367/581012,
                6: 20510/581012
            }
            with open(covtype_processed_data, 'r') as instance_file:
                instances_list = instance_file.readlines()
                self.dataset = []
                for line in instances_list:
                    # Convert the list in the string to a list
                    instance_as_list = ast.literal_eval(line)
                    self.dataset.append(instance_as_list)

    '''
    Returns true iff the possible attribute values are 0 or 1.
    '''
    def splitable_attribute(self, attribute):
        return len(self.attribute_values[attribute]) == 2

    '''
    Split the attribute by using the cutting value provided.
    The instances with attribute value less than or equal to the cutting point
    will have a new attribute value of 0; the rest of them will have 1 as the
    attribute value.
    '''
    def split_attribute(self, attribute, cutting_value):
        for instance in self.dataset:
            if instance[attribute] <= cutting_value:
                instance[attribute] = 0
            else:
                instance[attribute] = 1
        return self

    '''
    Find the best cutting value for an attribute from a random choice of 10
    possible values from the dataset.

    *** PRECONDITION ***: the attribute must be splitable
    '''
    def best_cutting_value(self, attribute):
        best_cutting_value = None
        best_profit = None

        if len(self.dataset) > 4:
            random_indices = random.sample(
                list(range(len(self.dataset))), 4)
        else:
            random_indices = list(range(len(self.dataset)))

        # k = int(len(self.dataset)/100000)
        # if k == 0:
        #     random_indices = list(range(len(self.dataset)))
        # else:
        #     random_indices = random.sample(list(range(len(self.dataset))), int(len(self.dataset)/100000))
        for i in random_indices:
            new_profit = Utils.profit(
                self.dataset, attribute, [self.dataset[i][attribute]],
                self.classes)
            if best_profit is None or new_profit > best_profit:
                best_profit = new_profit
                best_cutting_value = self.dataset[i][attribute]
        return best_cutting_value
    '''
    Project the instances across attribute, returning a list with instances of
    Data that doesn't share memory with the current instance.
    The instances of each Data instance returned share the same value of the
    attribute.
    '''
    def project_attribute(self, attribute):
        # A dictionary value -> instances with that value in attribute
        projections_dict = {}
        for value in self.attribute_values[attribute]:
            # Generate a copy of self
            projected_data = self.copy()
            # Adjust remaining attributes and amount of them
            projected_data.attributes.remove(attribute)
            projected_data.amount_attributes = self.amount_attributes - 1
            # Adjust dictionary of attribute -> values
            del projected_data.attribute_values[attribute]
            # Re initialize class distribution (computed later)
            for i in range(len(projected_data.class_distribution)):
                projected_data.class_distribution[projected_data.classes[i]] = 0.0

            projected_data.dataset = []
            # Add projected data to dictionary. It remains to filter the
            # instances and compute the class distributions for each new
            # instance of Data.
            projections_dict[value] = projected_data

        # Filter the instances and compute the class distributions
        # for each new instance of Data.
        for instance in self.dataset:
            # Check the value of the attribute
            instance_attribute_value = instance[attribute]
            projected_data = projections_dict[instance_attribute_value]
            # Copy the instance to the corresponding sub dataset
            projected_data.dataset.append(instance.copy())
            # Update the class distributions (divide by total number of
            # instances later)
            instance_class = instance[-1]
            projected_data.class_distribution[instance_class] += 1

        # Adjust the class distributions dividing by the number of instances
        for value in projections_dict:
            # Indicates if all instances belong to the same class
            monoclass_instances = True
            # Class label of the last instance viewed
            last_class_instance = None

            projected_data = projections_dict[value]
            for c in projected_data.class_distribution:
                instance_number = len(projected_data.dataset)
                if instance_number > 0:
                    projected_data.class_distribution[c] /= instance_number

                # Check if filtered instances belong to the same class
                if projected_data.class_distribution[c] > 0:
                    if last_class_instance is None:
                        last_class_instance = c
                    else:
                        if last_class_instance != c:
                            monoclass_instances = False

            # Set monoclass_instances attribute
            if monoclass_instances and last_class_instance is not None:
                projected_data.monoclass_instances = last_class_instance

        return projections_dict

    '''
    recalculates global and local distributions
    taking current dataset
    '''
    def recalculate_distributions(self):
        new_distribution = {}
        for c in self.classes:
            new_distribution[c] = 0
        for instance in self.dataset:
            new_distribution[instance[-1]] += 1
        for value in new_distribution.values():
            value /= len(self.dataset)
        self.global_class_distribution = new_distribution
        self.class_distribution = new_distribution

    '''
    creates both validation and training sets from data
    percentage takes values from 0 and 1
    '''
    def divide_corpus(self, percetnage_training):
        validation_set = self.dataset.copy()
        training_set = []
        partition_length = round(len(self.dataset) * percetnage_training)
        for i in range(0, partition_length):
            data_index = random.randint(0, len(validation_set)-1)
            training_set.append(validation_set[data_index])
            # data thats on training set cant be on validation set
            del validation_set[data_index]

        data_training = Data("iris")
        data_training.dataset = training_set
        data_training.data_name = self.data_name
        data_training.amount_attributes = self.amount_attributes
        data_training.attributes = self.attributes.copy()
        data_training.attribute_values = self.attribute_values.copy()
        data_training.amount_classes = self.amount_classes
        data_training.classes = self.classes.copy()
        data_training.class_distribution = self.class_distribution.copy()
        data_training.global_class_distribution = self.global_class_distribution.copy()

        data_validation = Data("iris")
        data_validation.dataset = validation_set
        data_validation.data_name = self.data_name
        data_validation.amount_attributes = self.amount_attributes
        data_validation.attributes = self.attributes.copy()
        data_validation.attribute_values = self.attribute_values.copy()
        data_validation.amount_classes = self.amount_classes
        data_validation.classes = self.classes.copy()
        data_validation.class_distribution = self.class_distribution.copy()
        data_validation.global_class_distribution = self.global_class_distribution.copy()
        return data_training, data_validation

    def apply_breakpoints(self, breakpoints):
        for attribute in breakpoints.keys():
            for data in self.dataset:
                if data[attribute] <= breakpoints[attribute]:
                    data[attribute] = 0
                else:
                    data[attribute] = 1

    def copy(self):
        data = Data('iris')     # Optimization
        data.dataset = copy.deepcopy(self.dataset)
        data.data_name = self.data_name
        data.amount_attributes = self.amount_attributes
        data.attributes = self.attributes.copy()
        data.attribute_values = self.attribute_values.copy()
        data.amount_classes = self.amount_classes
        data.classes = self.classes.copy()
        data.class_distribution = self.class_distribution.copy()
        data.global_class_distribution = self.global_class_distribution.copy()
        return data

    '''
    Saves the instances to the given file_path.
    '''
    def save_data(self, file_path):
        with open(file_path, 'w') as save_file:
            for instance in self.dataset:
                save_file.write(str(instance) + '\n')


'''
Loads the instances from the given file_path of the corresponding dataset.
Returns an instance of Data.
'''


def load_data(dataset_name, file_path):
    data = Data(dataset_name)
    data.dataset = []
    with open(file_path, 'r') as instances_file:
        instances_lines = instances_file.readlines()
        for instance_line in instances_lines:
            data.dataset.append(ast.literal_eval(instance_line))
    data.recalculate_distributions()
    return data

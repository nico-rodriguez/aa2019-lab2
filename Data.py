'''
Data module

This module's responsibility is to encapsule the parsed data as well as
metadata from the given dataset.
'''
import ast
import random
import Utils


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
        #print('Creating Data class instance')
        self.data_name = data_name
        # Indicates if all instances belong to the same class
        self.monoclass_instances = None
        if (data_name == "iris"):
            #print('Iris data selected')
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
            #print('Beginning iris data loading into Data instance')
            with open(iris_processed_data, 'r') as instance_file:
                instances_list = instance_file.readlines()
                self.dataset = []
                for line in instances_list:
                    # Convert the list in the string to a list
                    instance_as_list = ast.literal_eval(line)
                    self.dataset.append(instance_as_list)
        else:
            #print('Covtype data selected')
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
            #print('Beginning covtype data loading into Data instance')
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
        if len(self.dataset) > 10:
            random_indices = random.sample(
                list(range(len(self.dataset))), 10)
        else:
            random_indices = list(range(len(self.dataset)))

        for i in random_indices:
            new_profit = Utils.profit(
                self.dataset, attribute, [self.dataset[i][attribute]],
                self.classes)
            if best_profit is None or new_profit > best_profit:
                best_profit = new_profit
                best_cutting_value = self.dataset[i][attribute]
        '''
        for instance in self.dataset:
            new_profit = Utils.profit(
                self.dataset, attribute, [instance[attribute]], self.classes)
            if best_profit is None or new_profit > best_profit:
                best_profit = new_profit
                best_cutting_value = instance[attribute]
        '''

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
            # Don't parse files for the new Data instances
            projected_data = Data(self.data_name)
            # Adjust remaining attributes and amount of them
            projected_data.attributes = self.attributes.copy()
            projected_data.attributes.remove(attribute)
            projected_data.amount_attributes = self.amount_attributes - 1
            # Adjust dictionary of attribute -> values
            projected_data.attribute_values = self.attribute_values.copy()
            del projected_data.attribute_values[attribute]
            # Re initialize class distribution (computed later)
            for i in range(len(projected_data.class_distribution)):
                projected_data.class_distribution[i] = 0.0

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


if __name__ == '__main__':

    data = Data('iris')
    print(data.dataset[0:20])

    split_data = data.split_attribute(
        0, data.best_cutting_value(0)).project_attribute(0)
    with open('test.txt', 'w') as test_file:
        for instance in split_data[0].dataset:
            test_file.write(str(instance) + '\n')
        test_file.write('\n\n')
        for instance in split_data[1].dataset:
            test_file.write(str(instance) + '\n')
    '''
    data2 = Data('covtype')
    print(data2.dataset[0:20])
    '''

'''
Data module

This module's responsibility is to encapsule the parsed data as well as
metadata from the given dataset.
'''
import Parser
import ast


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
    def __init__(
            self, data_name, parse_dataset_files=True, instances_file=None):
        self.data_name = data_name
        # Indicates if all instances belong to the same class
        self.monoclass_instances = None
        if (data_name == "iris"):
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
            if parse_dataset_files:
                self.dataset = Parser.parse_data(
                    "iris/iris.data", 4, self.classes)
            else:
                if instances_file is None:
                    self.dataset = []
                else:
                    with open(instances_file, 'r') as processed_data:
                        instances_list = processed_data.readlines()
                        self.dataset = []
                        for line in instances_list:
                            self.dataset.append(ast.literal_eval(line))
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
            if parse_dataset_files:
                self.dataset = Parser.parse_data(
                    "covtype/covtype.data", 10, self.classes)
                self.dataset = Parser.process_binary(self.dataset)
            else:
                if instances_file is None:
                    self.dataset = []
                else:
                    with open(instances_file, 'r') as processed_data:
                        instances_list = processed_data.readlines()
                        self.dataset = []
                        for line in instances_list:
                            self.dataset.append(ast.literal_eval(line))

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
            projected_data = Data(self.data_name, False)
            # Adjust remaining attributes
            projected_data.attributes = self.attributes.copy()
            projected_data.attributes.remove(attribute)
            # Adjust dictionary of attribute -> values
            projected_data.attribute_values = self.attribute_values.copy()
            del projected_data.attribute_values[attribute]
            # Re initialize class distribution (computed later)
            for i in range(len(projected_data.class_distribution)):
                projected_data.class_distribution[i] = 0.0

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
    data = Data('iris', False, 'processed_data_iris.txt')
    print(data.dataset)
    data2 = Data('covtype', False, 'processed_data_covtype.txt')

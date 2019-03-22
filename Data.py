'''
Data module

This module's responsibility is to encapsule the parsed data as well as
metadata from the given dataset.
'''
import Parser


class Data:
    def __init__(self, data_name, parse_dataset_files=True):
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
            if parse_dataset_files:
                self.dataset = Parser.parse_data("iris/iris.data", 4)
            else:
                self.dataset = []
        else:
            # TODO: check number of attributes of dataset (dataset info states
            # that there are 12 attributes, divided into 54 columns)
            self.amount_attributes = 12
            self.attributes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            self.attribute_values = {
                0: [0, 1], 1: [0, 1], 2: [0, 1], 3: [0, 1], 4: [0, 1],
                5: [0, 1], 6: [0, 1], 7: [0, 1], 8: [0, 1], 9: [0, 1],
                10: [0, 1], 11: [0, 1]
            }
            self.amount_classes = 7
            self.classes = [0, 1, 2, 3, 4, 5, 6]
            self.class_distribution = {
                0: 211840/581012, 1: 283301/581012, 2: 35754/581012,
                3: 2747/581012, 4: 9493/581012, 5: 17367/581012,
                6: 20510/581012
            }
            if parse_dataset_files:
                self.dataset = Parser.parse_data("covtype/covtype.data", 7)
            else:
                self.dataset = []

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
            for c in projections_dict[value].class_distribution:
                instance_number = len(projections_dict[value].dataset)
                projections_dict[
                    value].class_distribution[c] /= instance_number
        return list(projections_dict.values)

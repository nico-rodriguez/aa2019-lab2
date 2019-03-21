'''
Data module

This module's responsibility is to encapsule the parsed data as well as
metadata from the given dataset.
'''
import Parser


class Data:
    def __init__(self, data_name):
        self.data_name = data_name
        if (data_name == "iris"):
            self.amount_attributes = 4
            self.attribute_values = {
                0: [0, 1], 1: [0, 1], 2: [0, 1], 3: [0, 1]
            }
            self.amount_classes = 3
            self.classes = [
                'Iris-setosa\n', 'Iris-versicolor\n', 'Iris-virginica\n'
            ]
            self.class_distribution = [1/3, 1/3, 1/3]
            self.dataset = Parser.parse_data("iris/iris.data", 4)
        else:
            # TODO: check number of attributes of dataset (dataset info states
            # that there are 12 attributes, divided into 54 columns)
            self.amount_attributes = 12
            self.attribute_values = {
                0: [0, 1], 1: [0, 1], 2: [0, 1], 3: [0, 1], 4: [0, 1],
                5: [0, 1], 6: [0, 1], 7: [0, 1], 8: [0, 1], 9: [0, 1],
                10: [0, 1], 11: [0, 1]
            }
            self.amount_classes = 7
            self.classes = [1, 2, 3, 4, 5, 6, 7]
            self.class_distribution = [
                211840/581012, 283301/581012, 35754/581012,
                2747/581012, 9493/581012, 17367/581012, 20510/581012
            ]
            self.dataset = Parser.parse_data("covtype/covtype.data", 7)

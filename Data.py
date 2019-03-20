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
            self.amount_classes = 3
            self.class_distribution = [1/3, 1/3, 1/3]
            self.dataset = Parser.parse_data("iris/iris.data", 4)
        else:
            self.amount_attributes = 10
            self.amount_classes = 7
            self.class_distribution = [
                211840/581012, 283301/581012, 35754/581012,
                2747/581012, 9493/581012, 17367/581012, 20510/581012
            ]
            self.dataset = Parser.parse_data("covtype/covtype.data", 7)

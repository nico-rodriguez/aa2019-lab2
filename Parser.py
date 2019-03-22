'''
Data parser module.

This module's responsibilty is to read datasets and process them into a data
structure.
'''

# Reads data from the file in "file_route"

import Utils
import Data


def parse_data(file_route, amount_attributes, classes):
    with open(file_route, "r") as file_to_parse:
        lines_of_data = file_to_parse.readlines()
    lines_of_split_data = []
    for line in lines_of_data:
        split_line = line.split(",")
        if ("iris" not in file_route):
            split_line[-1] = int(split_line[-1]) - 1
        else:
            split_line[-1] = split_line[-1].rstrip()
        lines_of_split_data.append(split_line)
    profits = []
    lines_of_split_data = lines_of_split_data[0:len(lines_of_split_data)-1]
    for atribute in range(0, amount_attributes):
        class_id = lines_of_split_data[0][amount_attributes]
        for split_line in lines_of_split_data:
            if (class_id != split_line[amount_attributes]):
                breakpoint_profit = Utils.profit(lines_of_split_data, atribute, [split_line[atribute]], classes)
                profits.append((breakpoint_profit, split_line[atribute]))
                class_id = split_line[amount_attributes]
        ideal_breakpoint = max(profits)
        for split_line in lines_of_split_data:
            if (float(split_line[atribute]) <= float(ideal_breakpoint[1])):
                split_line[atribute] = 0
            else:
                split_line[atribute] = 1
        profits = []
    return lines_of_split_data


def process_binary(lines_of_split_data):
    result_list = []
    for line in lines_of_split_data:
        copied_list = line[0:10].copy()
        first_binary_value = line[10:14].index("1")
        copied_list.append(first_binary_value)
        second_binary_value = line[14:54].index("1")
        copied_list.append(second_binary_value)
        copied_list.append(line[-1])
        result_list.append(copied_list)
    return result_list



if __name__ == "__main__":
    data = Data.Data("iris")
    with open("processed_data_iris.txt", "w") as outfile:
        for line in data.dataset:
            outfile.write(str(line) + "\n")

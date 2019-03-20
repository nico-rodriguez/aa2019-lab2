'''
Data parser module.

This module's responsibilty is to read datasets and process them into a data
structure.
'''

# Reads data from the file in "file_route"

import random
#from Utils.py import profit
import Data


def parse_data(file_route, amount_attributes):
    with open(file_route, "r") as file_to_parse:
        lines_of_data = file_to_parse.readlines()
    lines_of_split_data = []
    for line in lines_of_data:
        split_line = line.split(",")
        lines_of_split_data.append(split_line)
    class_id = lines_of_split_data[0][amount_attributes]
    profits = []
    lines_of_split_data = lines_of_split_data[0:len(lines_of_split_data)-1]
    for atribute in range(0, amount_attributes):
        for split_line in lines_of_split_data:
            print(split_line)
            if (class_id != split_line[amount_attributes]):
                breakpoint_profit = random.randint(1, 101)  #profit(lines_of_split_data, atribute, [split_line[atribute]])
                profits.append((breakpoint_profit, split_line[atribute]))
                class_id = split_line[amount_attributes]
        ideal_breakpoint = max(profits)
        print(profits)
        for split_line in lines_of_split_data:
            if ((float) (split_line[atribute]) <= ideal_breakpoint[0]):
                split_line[atribute] = 0
            else:
                split_line[atribute] = 1
    return lines_of_split_data


if __name__ == "__main__":
    data = Data.Data("iris")
    with open("processed_data.txt", "w") as outfile:
        for line in data.dataset:
            outfile.write(str(line) + "\n")

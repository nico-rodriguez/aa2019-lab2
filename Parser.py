'''
Data parser module.

This module's responsibilty is to read datasets and process them into a data
structure.
'''

import ast

'''
Reads data from the file in "file_route" and saves it as Python objects
to be read from Data class.
'''


def parse_data(file_route, amount_attributes, classes):
    with open(file_route, "r") as file_to_parse:
        lines_of_data = file_to_parse.readlines()
    lines_of_split_data = []
    print("File data loaded succesfully")
    print('Parsing dataset file')
    for line in lines_of_data:
        split_line = line.split(",")
        if ("iris" not in file_route):
            split_line[-1] = int(split_line[-1]) - 1
        else:
            split_line[-1] = split_line[-1].rstrip()
        for i in range(len(split_line)-1):
            split_line[i] = ast.literal_eval(split_line[i])
        lines_of_split_data.append(split_line)
    print('Finished parsing dataset file')
    return lines_of_split_data
    '''
    profits = []
    lines_of_split_data = lines_of_split_data[0:len(lines_of_split_data)-1]
    for atribute in range(0, amount_attributes):
        class_id = lines_of_split_data[0][amount_attributes]
        for idx, split_line in enumerate(lines_of_split_data, start=0):
            print("parsing atribute " + str(atribute) + " in line " + str(idx))
            if (class_id != split_line[amount_attributes]):
                breakpoint_profit = Utils.profit(
                    lines_of_split_data, atribute, [split_line[atribute]],
                    classes)
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
    '''


def process_binary(lines_of_split_data):
    print('Processing binary values of attribute')
    result_list = []
    for line in lines_of_split_data:
        copied_list = line[0:10].copy()
        first_binary_value = line[10:14].index(1)
        copied_list.append(first_binary_value)
        second_binary_value = line[14:54].index(1)
        copied_list.append(second_binary_value)
        copied_list.append(line[-1])
        result_list.append(copied_list)
    return result_list


if __name__ == "__main__":
    with open("processed_data_iris.txt", "w") as outfile:
        parsed_data = parse_data(
            'iris/iris.data', 4,
            ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
        for line in parsed_data:
            outfile.write(str(line) + '\n')

    with open("processed_data_covtype.txt", "w") as outfile:
        parsed_data = parse_data('covtype/covtype.data', 10, list(range(7)))
        parsed_data = process_binary(parsed_data)
        for line in parsed_data:
            outfile.write(str(line) + '\n')

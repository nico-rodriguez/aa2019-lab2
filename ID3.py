'''
ID3 implementation module


This module's responsibilty is to implement teh ID3 algorithm and write the
resulting tree in a given file. Data is passed preprocessed by Parser.py.
'''
import json
from treelib import Tree
from Utils import profit


# Saves the tree in treelib format into target_file in json format
def save_tree(tree, target_file):
    json_str = tree.to_json(with_data=True)
    print(json_str)
    # Process json_str to a propper json format for load_tree
    json_str = json_str.replace("\\", "")
    with open(target_file, 'w') as outfile:
        outfile.write(json_str)


# Creates a treelib recursively from a dictionary
def __dictionary_to_tree(dictionary):
    if dictionary != {}:
        tree = Tree()
        root = list(dictionary.keys())[0]
        print('root', root)
        if 'data' in list(dictionary[root].keys()):
            tree.create_node(root, root, data=dictionary[root]['data'])
        else:
            tree.create_node(root, root)
        for children_dict in dictionary[root]["children"]:
            children_name = list(children_dict.keys())[0]
            children_key_list = list(children_dict[children_name].keys())
            # Node is a leaf
            if 'children' not in children_key_list:
                if 'data' in children_key_list:
                    tree.create_node(children_name, children_name, parent=root,
                                     data=children_dict[children_name]['data'])
                else:
                    tree.create_node(children_name, children_name, parent=root)
            # Node is not leaf
            else:
                tree.paste(root, __dictionary_to_tree(children_dict))
        return tree
    else:
        return Tree()


# reads a json file and returns a treelib tree
def load_tree(target_file):
    with open(target_file, 'r') as infile:
        dictionary = json.load(infile)
    return __dictionary_to_tree(dictionary)


'''
Given data (an instance of the Data class),
returns a classification tree following ID3 algorithm.
'''


def ID3(data):
    return __ID3(data, None)


'''
ID3 algorithm.
Recursively receives the training examples and the remaining attributes to
process inside an instance of Data class.
data is an instance of Data class. It has the remaining attributes to process.
data.attributes is a list of indices that represent the remaining attributes.
Returns a decision tree of treelib type.
'''


def __ID3(data):
    # Ćreate a root
    tree = Tree()
    # All remaining instances belong to the same class
    if not(data.monoclass_instances is None):
        tree.create_node('Class {c}'.format(c=data.monoclass_instances))
        return tree
    # The are no attributes left
    if data.amount_attributes == 0:
        # First consider the case where there are no examples left
        if len(data.dataset) == 0:
            # TODO: any label is likely
            pass
        # If there are examples left, sort the label according to the
        # class distribution known by the parent node
        else:
            # TODO: use data.class_distribution to label
            pass
    # There are attributes left
    elif data.amount_attributes > 0:
        # Choose best attribute
        best_root_attribute = None
        best_profit = None
        for attribute in data.attributes:
            new_profit = profit(data.dataset, attribute,
                                data.attribute_values[attribute],
                                data.classes)
            # TODO: how do we handle attributes with equal profit?
            if (best_profit is None) or (new_profit > best_profit):
                best_profit = new_profit
                best_root_attribute = attribute
        # Generate a branch for each possible value of the attribute
        for value in data.attribute_values:
            filtered_data = data.project_attribute(best_root_attribute, value)
            # If there are no examples left, sort the label according to the
            # class distribution known by the parent node
            if len(filtered_data.dataset) == 0:
                # TODO use filtered_data.class_distribution to label
                pass
            # Recursive call
            elif len(filtered_data.dataset) > 0:
                # TODO: create root node for this case
                child = __ID3(filtered_data)
                # TODO: attach child to parent
        return tree


    # Exception
    else:
        return "ID3.__ID3: data.amount_attributes can't be negative."


if __name__ == "__main__":
    tree = Tree()
    tree.create_node("Harry", "harry", data=[3, 2, 1])  # root node
    assert tree.get_node('harry').is_leaf()
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Mark", "mark", parent="jane", data=[0, 1, 2])
    save_tree(tree, "test.json")
    tree_test = load_tree("test.json")
    print(tree)
    print(tree.leaves())
    # tree_test.paste('Mark', Tree())
    print(tree_test)
    save_tree(tree_test, "test2.json")
    print(tree_test.leaves())
    assert tree_test.get_node('Mark').is_leaf()

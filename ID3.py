'''
ID3 implementation module


This module's responsibilty is to implement teh ID3 algorithm and write the
resulting tree in a given file. Data is passed preprocessed by Parser.py.
The tags in the nodes of the tree are the names of the attributes for the
current decision, if the node is not a leaf; if the node is a leaf, the tag
is the class label.
The identifiers of the nodes are the values of the attribute labeled in the
parent node (None for root).
Example:
                                    (tag=a3, id=None)
                                   /                 \
                    (tag=a1, id = v31)          (tag=a2, id=v32)
                    /                \                  |
            (tag=c2, id v11)    (tag=c1, id=v12)    (tag=c3, id=v21)
'''
import json
from treelib import Tree
from Utils import profit, weighted_random
import random


# Saves the tree in treelib format into target_file in json format
def save_tree(tree, target_file):
    # Process the tags of the nodes for loading the tree later
    # Each node's tag will be saved as tag + id
    nodes = tree.all_nodes()
    for node in nodes:
        node.tag = node.tag + ',' + node.identifier
    json_str = tree.to_json()
    # Process json_str to a proper json format for load_tree
    json_str = json_str.replace("\\", "")
    with open(target_file, 'w') as outfile:
        outfile.write(str(json_str))


# Creates a treelib recursively from a dictionary
def __dictionary_to_tree(node_info, tree):
    if isinstance(node_info, dict):
        root = list(node_info.keys())[0]
        # Split node tag from node id
        test = root.split(',')
        node_tag = root.split(',')[0]
        node_id = ','.join(root.split(',')[1:])
        parent_id = ','.join(root.split(',')[1:-2]) + ','
        if parent_id == ',':
            parent_id = None
        tree.create_node(node_tag, node_id, parent=parent_id)
        for children in node_info[root]["children"]:
            __dictionary_to_tree(children, tree)
    else:
        # Split node tag from node id
        node_name = node_info
        test = node_name.split(',')
        node_tag = ','.join(node_name.split(',')[0:2]) + ','
        node_id = ','.join(node_name.split(',')[2:])
        parent_id = ','.join(node_name.split(',')[2:-2]) + ','
        if parent_id == ',':
            parent_id = None
        tree.create_node(node_tag, node_id, parent=parent_id)
        return tree
    return tree


# reads a json file and returns a treelib tree
def load_tree(target_file):
    with open(target_file, 'r') as infile:
        dictionary = json.load(infile)
    return __dictionary_to_tree(dictionary, Tree())


'''
Given data (an instance of the Data class), returns a classification tree
following an extension of the ID3 algorithm and the cutting points generated.
'''


def ID3(data):
    tree = Tree()
    return __ID3(tree, data, None, None, None, {}, 0)


'''
ID3 algorithm.
Recursively receives the training examples and the remaining attributes to
process inside an instance of Data class.
data is an instance of Data class. It has the remaining attributes to process.
data.attributes is a list of indices that represent the remaining attributes.
Returns a decision tree of treelib type.
'''


def __ID3(tree, data, parent_attribute, parent_attribute_value,
          path_to_parent, cutting_values, depth):
    if depth >= 3:
        random_class = weighted_random(data.classes, data.class_distribution)
        tree.create_node('Class {c},Instances {inst}'.format(
                c=random_class, inst=len(data.dataset)),
                            path_to_parent + 'Attribute {attr} = {val}'.format(
                            attr=parent_attribute, val=parent_attribute_value)
                            + ",", path_to_parent)
        return tree, cutting_values
    else:
        depth += 1
        parent_id = path_to_parent
        if path_to_parent is None:
            path_to_parent = ""
        # All remaining instances belong to the same class
        if data.monoclass_instances is not None:
            tree.create_node('Class {c},Instances {inst}'.format(
                c=data.monoclass_instances, inst=len(data.dataset)),
                            path_to_parent + 'Attribute {attr} = {val}'.format(
                            attr=parent_attribute, val=parent_attribute_value)
                            + ",", parent_id)
            return tree, cutting_values
        # The are no attributes left
        if data.amount_attributes == 0:
            # First consider the case where there are no examples left
            if len(data.dataset) == 0:
                # Any label is likely (check data.global_class_distribution)
                sorted_class = weighted_random(data.classes,
                                            data.global_class_distribution)
                tree.create_node('Class {c},Instances {inst}'.format(
                    c=sorted_class, inst=0), path_to_parent +
                    'Attribute {attr} = {val}'.format(
                        attr=parent_attribute,
                        val=parent_attribute_value) + ",", parent_id)
                return tree, cutting_values
            # If there are examples left, sort the label according to the
            # class distribution known by the parent node
            else:
                # Use data.class_distribution to label
                sorted_class = weighted_random(
                    data.classes, list(data.class_distribution.values()))
                tree.create_node('Class {c},Instances {inst}'.format(
                    c=sorted_class, inst=len(data.dataset)), path_to_parent +
                    'Attribute {attr} = {val}'.format(
                        attr=parent_attribute, val=parent_attribute_value) +
                    ",", parent_id)
                return tree, cutting_values
        # There are attributes left
        if data.amount_attributes > 0:
            # Shorten the tree depth to total_attribute_number / 2 in case of covtype dataset
            if len(data.dataset) == 0:
                # Any label is likely (check data.global_class_distribution)
                sorted_class = weighted_random(
                    data.classes, list(data.global_class_distribution.values()))
                tree.create_node('Class {c},Instances {inst}'.format(
                    c=sorted_class, inst=0), path_to_parent +
                    'Attribute {attr} = {val}'.format(
                        attr=parent_attribute, val=parent_attribute_value) + ",",
                    parent_id)
                return tree, cutting_values
            else:
                # Choose best attribute
                best_root_attribute_list = []
                best_profit = None
                spliting_value_for_attribute = {}
                for attribute in data.attributes:
                    if data.splitable_attribute(attribute):
                        spliting_value_for_attribute[attribute] = (
                            data.best_cutting_value(attribute))
                        new_profit = profit(data.dataset, attribute,
                                            [spliting_value_for_attribute[
                                                attribute]],
                                            data.classes)
                    else:
                        new_profit = profit(data.dataset, attribute,
                                            data.attribute_values[attribute],
                                            data.classes)
                    # If more than one attributes have equal profit,
                    # choose one at random
                    if (best_profit is None) or (new_profit > best_profit):
                        best_profit = new_profit
                        best_root_attribute_list = [attribute]
                    elif best_profit == new_profit:
                        best_root_attribute_list.append(attribute)

                best_root_attribute = random.choice(best_root_attribute_list)
                # Create root node for this case
                tree.create_node('Attribute {attr}'.format(
                    attr=best_root_attribute),
                    path_to_parent + 'Attribute {attr} = {val}'.format(
                    attr=parent_attribute, val=parent_attribute_value) + ",",
                    parent_id)
                if data.splitable_attribute(best_root_attribute):
                    data.split_attribute(best_root_attribute,
                                         spliting_value_for_attribute[
                                            best_root_attribute])
                    cutting_values[best_root_attribute] = (
                        spliting_value_for_attribute[best_root_attribute])
                # Generate a branch for each possible value of the attribute
                filtered_data_dict = data.project_attribute(best_root_attribute)
                for value in data.attribute_values[best_root_attribute]:
                    # If there are no examples left, sort the label according to
                    # the class distribution known by the parent node
                    if len(filtered_data_dict[value].dataset) == 0:
                        # Use filtered_data_dict[value].class_distribution to label
                        sorted_class = weighted_random(
                            data.classes,
                            data.global_class_distribution)
                        tree.create_node('Class {c},Instances {inst}'.format(
                            c=sorted_class, inst=len(data.dataset)), path_to_parent
                            + 'Attribute {attr} = {val},'.format(
                                attr=parent_attribute, val=parent_attribute_value)
                            + 'Attribute {attr} = {val}'.format(
                            attr=best_root_attribute, val=value) + ",",
                            parent_id + 'Attribute {attr} = {val},'.format(
                                attr=parent_attribute, val=parent_attribute_value))
                        return tree, cutting_values
                    # Recursive call
                    elif len(filtered_data_dict[value].dataset) > 0:
                        __ID3(tree, filtered_data_dict[value],
                            best_root_attribute, value, path_to_parent +
                            "Attribute {attr} = {val}".format(
                            attr=parent_attribute,
                            val=parent_attribute_value) + ",", cutting_values, depth)
                return tree, cutting_values
        # Exception
        else:
            return "ID3.__ID3: data.amount_attributes can't be negative."

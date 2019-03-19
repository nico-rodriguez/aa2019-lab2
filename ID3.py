'''
ID3 implementation module


This module's responsibilty is to implement teh ID3 algorithm and write the
resulting tree in a given file. Data is passed preprocessed by Parser.py.
'''
import json
from treelib import Tree


# Saves the tree in treelib format into target_file in json format
def save_tree(tree, target_file):
    json_str = tree.to_json()
    # Process json_str to a propper json format for load_tree
    json_str = json_str.replace("\\", "")
    print(json_str)
    with open(target_file, 'w') as outfile:
        outfile.write(json_str)


# Creates a treelib recursively from a dictionary
def dictionary_to_tree(dictionary):
    if dictionary != {}:
        tree = Tree()
        root = list(dictionary.keys())[0]
        tree.create_node(root, root)
        for value in dictionary[root]["children"]:
            if (isinstance(value, dict)):
                tree.paste(root, dictionary_to_tree(value))
            else:
                tree.create_node(value, value, parent=root)
        return tree
    else:
        return Tree()


# reads a json file and returns a treelib tree
def load_tree(target_file):
    with open(target_file, 'r') as infile:
        dictionary = json.load(infile)
        print(type(dictionary))
    return dictionary_to_tree(dictionary)


if __name__ == "__main__":
    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Mark", "mark", parent="jane")
    save_tree(tree, "test.json")
    tree_test = load_tree("test.json")
    print(tree)
    print(tree_test)

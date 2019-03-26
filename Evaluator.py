'''
Evaluator module

This module's responsibilty is to evaluate the quality of a given tree
over a given preprocessed data set.
'''

import Classifier

'''
This function evaluates a given tree's metrics: true positives, true negatives,
false positives, false negatives, precision, recall, fall-off and F-measure.
verification_data is an instance of Data used to compute the metrics.
It saves the metrics and the confusion matrix to a given file's path.
'''


def evaluate_tree(tree, verification_data, file_path):
    '''
    Dictionary of dictionaries. confusion_matrix[class] has a dictionary
    with the instance number of each class.
    confusion_matrix[class_i][class_j] is the number of instances from
    class_i classified as class_j.
    '''
    confusion_matrix = {}
    # Initialize confusion_matrix
    for c1 in verification_data.classes:
        confusion_matrix[c1] = {}
        for c2 in verification_data.classes:
            confusion_matrix[c1][c2] = 0

    for instance in verification_data.dataset:
        classified_class_node_tag = Classifier.classify(tree, instance)

        classified_class = classified_class_node_tag.split('Class ')[1]
        true_class = str(verification_data.dataset[-1])

        confusion_matrix[true_class][classified_class] += 1

    with open(file_path, 'w') as output:
        spaces = 15
        output.write('Confusion Matrix\n\n')
        output.write(' '*spaces + 'Actual class\n')
        output.write(' '*spaces)
        classes = list(verification_data.classes.keys())
        for c in classes:
            output.write('%{spaces}s'.format(spaces=spaces) % c)

        output.write('\n')
        for c1 in classes:
            output.write('%{spaces}s{c}'.format(spaces=spaces, c=c1))
            for c2 in classes:
                output.write('%{spaces}s{num}'.format(
                    spaces=spaces, num=confusion_matrix[c1][c2]))
            output.write('\n')

        output.write('\n')
        for c in classes:
            output.write('Metrics for class {c} classification\n'.format(c=c))

            true_positives = confusion_matrix[c][c]
            output.write('True Positives = {val}'.format(val=true_positives))

            false_positives, false_negatives = 0, 0
            for c2 in classes:
                if c != c2:
                    false_positives += confusion_matrix[c][c2]
                    false_negatives += confusion_matrix[c2][c]
            output.write('False Positives = {val}'.format(val=false_positives))
            output.write('False Negatives = {val}'.format(val=false_negatives))

            true_negatives = 0
            for c1 in classes:
                for c2 in classes:
                    if c1 != c and c2 != c:
                        true_negatives += confusion_matrix[c1][c2]
            output.write('True Negatives = {val}'.format(val=true_negatives))


if __name__ == '__main__':
    pass

'''
Evaluator module

This module's responsibilty is to evaluate the quality of a given tree
over a given preprocessed data set.
'''

import Classifier
import Data


'''
This function evaluates a given classifier's metrics: true positives,
true negatives, false positives, false negatives, precision, recall, fall-out
and F-measure.
It saves the metrics and the confusion matrix to a given file's path.
- 'classification' is a list of tuples (true_class, classified_class).
- 'classes' is a list with all the possible class labels.
- 'instances' is a list of instances (a list of lists) corresponding to the
verification instances.
- 'instances_number' is the number of instances in 'instances'.
- 'file_path' is the route to the file for saving the evaluation metrics.
'''


def evaluate_classificator(classification, classes,
                           instances, instances_number,
                           file_path):
    '''
    Dictionary of dictionaries: confusion_matrix[class] has a dictionary
    with the instance number of each class.
    confusion_matrix[class_i][class_j] is the number of instances from
    class_i classified as class_j.
    '''
    confusion_matrix = {}
    # Initialize confusion_matrix
    for c1 in classes:
        confusion_matrix[c1] = {}
        for c2 in classes:
            confusion_matrix[c1][c2] = 0

    # Amount of examples of each class
    amount_instances = {}
    for c in classes:
        amount_instances[c] = 0

    for instance in instances:
        amount_instances[str(instance[-1])] += 1

    for true_class, classified_class in classification:
        confusion_matrix[str(classified_class)][str(true_class)] += 1

    precision_macro, recall_macro, fall_out_macro, f_measure_macro = 0, 0, 0, 0
    precision_micro, recall_micro, fall_out_micro, f_measure_micro = 0, 0, 0, 0
    with open(file_path, 'w') as output:
        spaces = 16
        output.write('Confusion Matrix\n')
        output.write(' '*(spaces + 4) + 'Actual class\n')
        output.write(' '*spaces)
        for c in classes:
            output.write('%{spaces}s'.format(spaces=spaces) % c)
        output.write('\n')
        for c1 in classes:
            output.write('%{spaces}s'.format(spaces=spaces) % c1)
            for c2 in classes:
                output.write('%{spaces}d'.format(
                    spaces=spaces) % confusion_matrix[c1][c2])
            output.write('\n')

        output.write('\n')
        for c1 in classes:
            for c2 in classes:
                output.write('%{spaces}d'.format(
                    spaces=spaces) % confusion_matrix[c1][c2])
            output.write('\n')

        output.write('\n')

        output.write('Metrics for a given class\n')
        output.write('True Positives\n')
        output.write('False Positives\n')
        output.write('False Negatives\n')
        output.write('True Negatives\n')
        output.write('Precision\n')
        output.write('Recall\n')
        output.write('Fall-out\n')
        output.write('F-Measure\n')

        output.write('\n')
        for c in classes:
            output.write('Metrics for class {c} classification\n'.format(c=c))

            true_positives = confusion_matrix[c][c]
            output.write('{val}\n'.format(val=true_positives))

            false_positives, false_negatives = 0, 0
            for c2 in classes:
                if c != c2:
                    false_positives += confusion_matrix[c][c2]
                    false_negatives += confusion_matrix[c2][c]
            output.write('{val}\n'.format(
                val=false_positives))
            output.write('{val}\n'.format(
                val=false_negatives))

            true_negatives = 0
            for c1 in classes:
                for c2 in classes:
                    if c1 != c and c2 != c:
                        true_negatives += confusion_matrix[c1][c2]
            output.write('{val}\n'.format(val=true_negatives))

            if true_positives == 0:
                precision = 0.0
            else:
                precision = true_positives/(true_positives+false_positives)
            output.write('{val}\n'.format(val=precision))

            if true_positives == 0:
                recall = 0.0
            else:
                recall = true_positives/(true_positives+false_negatives)
            output.write('{val}\n'.format(val=recall))

            if false_positives == 0:
                fall_out = 0.0
            else:
                fall_out = false_positives/(false_positives+true_negatives)
            output.write('{val}\n'.format(val=fall_out))

            if precision == 0 or recall == 0:
                f_measure = 0
            else:
                f_measure = 1/((0.5/precision) + (0.5/recall))
            output.write('{val}\n'.format(val=f_measure))

            precision_macro += precision
            recall_macro += recall
            fall_out_macro += fall_out
            f_measure_macro += f_measure

            precision_micro += amount_instances[c]*precision
            recall_micro += amount_instances[c]*recall
            fall_out_micro += amount_instances[c]*fall_out
            f_measure_micro += amount_instances[c]*f_measure

            output.write('\n\n')

        class_number = len(classes)

        precision_macro /= class_number
        recall_macro /= class_number
        fall_out_macro /= class_number
        f_measure_macro /= class_number

        precision_micro /= instances_number
        recall_micro /= instances_number
        fall_out_micro /= instances_number
        f_measure_micro /= instances_number

        output.write('Macro measures\n')
        output.write('Precision\n')
        output.write('Recall\n')
        output.write('Fall-out\n')
        output.write('F-Measure\n')
        output.write('{val}\n'.format(val=precision_macro))
        output.write('{val}\n'.format(val=recall_macro))
        output.write('{val}\n'.format(val=fall_out_macro))
        output.write('{val}\n'.format(val=f_measure_macro))

        output.write('\n\n')

        output.write('Micro measures\n')
        output.write('Precision\n')
        output.write('Recall\n')
        output.write('Fall-out\n')
        output.write('F-Measure\n')
        output.write('{val}\n'.format(val=precision_micro))
        output.write('{val}\n'.format(val=recall_micro))
        output.write('{val}\n'.format(val=fall_out_micro))
        output.write('{val}\n'.format(val=f_measure_micro))

        output.write('\n')


if __name__ == '__main__':
    data = Data.Data('iris')
    (data_training, data_validation) = data.divide_corpus(0.8)
    classifier = Classifier.generate_forest_classifier(data_training)
    modified_data_validations = []
    for elem in classifier:
        new_validation_data = data_validation.copy()
        new_validation_data.apply_breakpoints(elem[1])
        modified_data_validations.append(new_validation_data)
    classification = Classifier.classify_dataset_multi_label(classifier, modified_data_validations)
    evaluate_classificator(classification, data_validation.classes,
                           data_validation.dataset,
                           len(data_validation.dataset), 'Evaluator.out')
'''
Main module of the project.
'''

import Classifier
import Data
import Evaluator
import ID3
import os
import sys

training_file_name = 'training.txt'
validation_file_name = 'validation.txt'
classifier_file_name_prefix = 'classifier'

if __name__ == '__main__':
    uso = """
        Hay dos modos de uso: Entrenar y Evaluar. El primero genera el clasificador y separa las instancias
        para entrenamiento y para verificación; el segundo evalúa un clasificador generado previamente con
        el modo Entrenar.

        Para Entrenar invocar como

        python3 Main.py Entrenar [iris|covtype] [Single|Forest] [training] [directorio]

        donde:
        - iris o covtype indica el nombre del dataset que se utilizará.
        - Single indica que se entrena un único árbol de decision multi-clase
        y Forest indica que se entrena un clasificador formado por árboles que
        clasifican una clase versus el resto.
        - training indica la proporción de las instancias que serán destinadas
        a entrenamiento; las restantes son destinadas a verificación. Debe ser
        un número entre 0 y 1 (e.g. 0.8).
        - directorio es el nombre del directorio en donde se van a guardar el clasificador
        y los archivos de instancias (se guardan las de entrenamiento y verificación en dos
        archivos diferentes). No debe existir otro directorio con el mismo nombre.

        Para Evaluar invocar como:

        python3 Main.py Evaluar [iris|covtype] [directorio]

        donde:
        - directorio es un directorio generado tal como se genera con el modo Entrenar (para que funcione
        correctamente, no se pueden modificar los archivos de dicho directorio).\n
    """

    # Sanitize arguments
    mode = sys.argv[1]
    if mode == 'Entrenar':
        dataset_name = sys.argv[2]
        if dataset_name not in ['iris', 'covtype']:
            print('Error. Nombre de dataset incorrecto. Solo puede ser "iris" o "covtype"\n')
            print(uso)
            exit()
        classifier_type = sys.argv[3]
        if classifier_type not in ['Single', 'Forest']:
            print('Error. Tipo de clasificador incorrecto. Solo puede ser "Single" o "Forest"\n')
            print(uso)
            exit()
        training_percentage = int(sys.argv[4])
        if training_percentage <= 0 or training_percentage >= 1:
            print('Error. Valor de proporción de instancias de entrenamiento' +
                  ' incorrecto. Solo puede ser un numero entre 0 y 1 (e.g. 0.8)\n')
            print(uso)
            exit()
        directory = sys.argv[5]
        if os.path.isdir(directory):
            print('Error. Ya existe el directorio especificado. Especificar uno nuevo.\n')
            print(uso)
            exit()

        # Create directory for saving the results
        print('Creando directorio {dir}\n'.format(dir=directory))
        os.mkdir(directory)

        # Read instances
        print('Leyendo dataset\n')
        data = Data.Data(dataset_name)

        # Divide corpus and save the training and validation instances
        print('Dividiendo corpus en {training}% para entrenamiento y {validation}% para validar\n'
              .format(training=training_percentage*100, validation=100-(training_percentage*100)))
        data_training, data_validation = data.divide_corpus(training_percentage)

        # Save the training and validation instances for later
        print('Guardando las instancias de entrenamiento y validación\n')
        data_training.save_data(directory + '/' + training_file_name)
        data_validation.save_data(directory + '/' + validation_file_name)

        # Generate classifier
        print('Entrenando al clasificador\n')
        if classifier_type == 'Single':
            tree = ID3.ID3(data_training)
            classifier_file_name = directory + '/' + classifier_file_name_prefix + '0.json'
            print('Guardando el clasificador en {file}\n'.format(file=classifier_file_name))
            ID3.save_tree(tree, classifier_file_name)
            exit()
        elif classifier_type == 'Forest':
            trees = Classifier.generate_forest_classifier(data_training)
            print('Guardando los árboles que componen al clasificador en el directorio {dir}'.format(dir=directory))
            for i in range(len(trees)):
                tree_file_name = directory + '/' + classifier_file_name_prefix + str(i) + '.json'
                print('Guardando árbol del clasificador en {file}\n'.format(file=tree_file_name))
                ID3.save_tree(trees[i], tree_file_name)
                exit()
        else:
            print('Main.py: Exception, impossible case.\n')

    elif mode == 'Evaluar':
        dataset_name = sys.argv[2]
        if dataset_name not in ['iris', 'covtype']:
            print('Error. Nombre de dataset incorrecto. Solo puede ser "iris" o "covtype"\n')
            print(uso)
            exit()
        directory = sys.argv[3]
        if not os.path.isdir(directory):
            print('Error. No existe el directorio especificado. Especificar un directorio que haya sido creado con el modo Entrenar.\n')
            print(uso)
            exit()

        # Load validation data
        print('Leyendo instancias para validar\n')
        data = Data.load_data(dataset_name, directory + '/' + validation_file_name)

        trees = []

        # Walk through the tree files inside the directory
        for root, dirs, files in os.walk(directory):
            # Load the tree(s) from the files "classifier0.json", "classifier1.json", etc.
            for i in range(data.amount_classes):
                tree_file_name = classifier_file_name_prefix + str(i) + '.json'
                if tree_file_name in files:

    else:
        print('Error. Modo de uso inválido. Los posibles modos de uso son Entrenar y Evaluar\n')
        print(uso)
        exit()

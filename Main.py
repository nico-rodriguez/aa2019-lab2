'''
Main module of the project.
'''

import ast
import Classifier
import copy
import Data
import Evaluator
import ID3
import os
import sys

training_file_name = 'training.txt'
validation_file_name = 'validation.txt'
classifier_file_name_prefix = 'classifier'
breakpoints_file_name_prefix = 'breakpoints'
distribution_file_name_prefix = 'distribution'
evaluation_file_name = 'evaluation.txt'

if __name__ == '__main__':
    uso_general = """
        Hay tres modos de uso: Entrenar, Evaluar y EvaluarAleatorio. El primero genera el clasificador y separa las instancias
        para entrenamiento y para verificación; el segundo evalúa un clasificador generado previamente con
        el modo Entrenar y el tercero evalúa un clasificador aleatorio que sortea las etiquetas de clase basándose en
        la cantidad de instancias que hay de cada clase.\n
    """
    uso_entrenar = """
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
        archivos diferentes). No debe existir otro directorio con el mismo nombre.\n
    """
    uso_evaluar = """
        Para Evaluar invocar como:

        python3 Main.py Evaluar [iris|covtype] [directorio]

        donde:
        - directorio es un directorio generado tal como se genera con el modo Entrenar (para que funcione
        correctamente, no se pueden modificar los archivos de dicho directorio). Los resultados de la evaluación
        se guardan en un archivo dentro de ese mismo directorio.\n
    """
    uso_evaluar_aleatorio = """
        Para EvaluarAleatorio invocar como:

        python3 Main.py EvaluarAleatorio [iris|covtype] [validation] [salida]

        donde:
        - validation es la proporción de instancias del dataset seleccionado que se van a utilizar
        para calcular las métricas.
        - salida es el nombre del archivo en donde se escriben las métricas de la evaluación.\n
    """

    # Sanitize arguments
    if len(sys.argv) < 4:
        print(uso_general + uso_entrenar + uso_evaluar + uso_evaluar_aleatorio)
        exit()

    mode = sys.argv[1]
    if mode == 'Entrenar':
        if len(sys.argv) != 6:
            print('Error. Número incorrecto de parámetros.\n')
            print(uso_entrenar)
            exit()
        dataset_name = sys.argv[2]
        if dataset_name not in ['iris', 'covtype']:
            print('Error. Nombre de dataset incorrecto. Solo puede ser "iris" o "covtype"\n')
            print(uso_entrenar)
            exit()
        classifier_type = sys.argv[3]
        if classifier_type not in ['Single', 'Forest']:
            print('Error. Tipo de clasificador incorrecto. Solo puede ser "Single" o "Forest"\n')
            print(uso_entrenar)
            exit()
        training_percentage = float(sys.argv[4])
        if training_percentage <= 0 or training_percentage > 1:
            print('Error. Valor de proporción de instancias de entrenamiento' +
                  ' incorrecto. Solo puede ser un numero entre 0 y 1, 1 inclusive (e.g. 0.8)\n')
            print(uso_entrenar)
            exit()
        directory = sys.argv[5]
        if os.path.isdir(directory):
            print('Error. Ya existe el directorio especificado. Especificar uno nuevo.\n')
            print(uso_entrenar)
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
            tree, breakpoints = ID3.ID3(data_training)
            classifier_file_name = directory + '/' + classifier_file_name_prefix + '0.json'
            print('Guardando el clasificador en {file}\n'.format(file=classifier_file_name))
            ID3.save_tree(tree, classifier_file_name)
            print('Guardando los breakpoints de los atributos con valores continuos\n')
            with open(directory + '/' + breakpoints_file_name_prefix + '.txt', 'w') as breakpoints_file:
                breakpoints_file.write(str(breakpoints))
            print(tree)
            exit()
        elif classifier_type == 'Forest':
            trees = Classifier.generate_forest_classifier(data_training)
            print('Guardando los árboles que componen al clasificador en el directorio {dir}'.format(dir=directory))
            for i in range(len(trees)):
                tree_file_name = directory + '/' + classifier_file_name_prefix + str(i) + '.json'
                print('Guardando árbol del clasificador en {file}\n'.format(file=tree_file_name))
                ID3.save_tree(trees[i][0], tree_file_name)
                breakpoints_file_name = directory + '/' + breakpoints_file_name_prefix + str(i) + '.txt'
                print('Guardando los breakpoints de los atributos con valores continuos en {file}'.format(file=breakpoints_file_name))
                with open(breakpoints_file_name, 'w') as breakpoints_file:
                    breakpoints_file.write(str(trees[i][1]))
                distribution_file_name = directory + '/' + distribution_file_name_prefix + str(i) + '.txt'
                print('Guardando distribuciones de clases para votación en {file}'.format(file=distribution_file_name))
                with open(distribution_file_name, 'w') as distribution_file:
                    distribution_file.write(str(trees[i][2]))
            exit()
        else:
            print('Main.py: Exception, impossible case.\n')

    elif mode == 'Evaluar':
        if len(sys.argv) != 4:
            print('Error. Número incorrecto de parámetros.\n')
            print(uso_evaluar)
            exit()
        dataset_name = sys.argv[2]
        if dataset_name not in ['iris', 'covtype']:
            print('Error. Nombre de dataset incorrecto. Solo puede ser "iris" o "covtype"\n')
            print(uso_evaluar)
            exit()
        directory = sys.argv[3]
        if not os.path.isdir(directory):
            print('Error. No existe el directorio especificado. Especificar un directorio que haya sido creado con el modo Entrenar.\n')
            print(uso_evaluar)
            exit()

        # Load validation data
        print('Leyendo instancias para validar\n')
        data_validation = Data.load_data(dataset_name, directory + '/' + validation_file_name)

        trees = []
        breakpoints = []
        distributions = []

        # Walk through the tree files inside the directory
        for root, dirs, files in os.walk(directory):
            # Load the tree(s) from the files "classifier0.json", "classifier1.json", etc.
            for i in range(data_validation.amount_classes):
                tree_file_name = classifier_file_name_prefix + str(i) + '.json'
                if tree_file_name in files:
                    print('Cargando árbol del archivo {file}'.format(file=directory + '/' + tree_file_name))
                    trees.append(ID3.load_tree(directory + '/' + tree_file_name))
                else:
                    break
                breakpoints_file_name = breakpoints_file_name_prefix + str(i) + '.txt'
                if breakpoints_file_name in files:
                    print('Cargando breakpoints del archivo {file}'.format(file=directory + '/' + breakpoints_file_name))
                    with open(directory + '/' + breakpoints_file_name, 'r') as breakpoints_file:
                        breakpoints.append((ast.literal_eval((breakpoints_file.read()))))
                distribution_file_name = distribution_file_name_prefix + str(i) + '.txt'
                if distribution_file_name in files:
                    print('Cargando distribuciones de clases del archivo {file}'.format(file=directory + '/' + distribution_file_name))
                    with open(directory + '/' + distribution_file_name, 'r') as distribution_file:
                        distributions.append((ast.literal_eval((distribution_file.read()))))

        # Single tree classifier
        if len(trees) == 1:
            # Load breakpoints
            print('Cargando breakpoints generados durante el entrenamiento\n')
            with (open(directory + '/' + breakpoints_file_name_prefix + '.txt')) as breakpoints_file:
                breakpoints = ast.literal_eval(breakpoints_file.read())
            print('Aplicando breakpoints a los atributos continuos de las instancias de validación\n')
            data_validation.apply_breakpoints(breakpoints)
            print('Ejecutando el clasificador sobre las instancias de validación\n')
            classification = Classifier.classify_dataset_tree(trees[0], data_validation)
        # Forest classifier
        else:
            classifier = []
            assert len(trees) == len(breakpoints) and len(breakpoints) == len(distributions)
            for i in range(len(trees)):
                classifier.append((trees[i], breakpoints[i], distributions[i]))
            data_validation_list = []
            for i in range(len(trees)):
                data_validation_list.append(copy.deepcopy(data_validation))
            print('Ejecutando el clasificador sobre las instancias de validación\n')
            classification = Classifier.classify_dataset_multi_label(classifier, data_validation_list)

        print('Evaluando clasificador\n')
        print('Guardando métricas en {file}'.format(file=directory + '/' + evaluation_file_name))
        classes = []
        for c in data_validation.classes:
            classes.append(str(c))
        Evaluator.evaluate_classificator(classification, classes,
                                         data_validation.dataset, len(data_validation.dataset),
                                         directory + '/' + evaluation_file_name)
        exit()
    elif mode == 'EvaluarAleatorio':
        if len(sys.argv) != 5:
            print('Error. Número incorrecto de parámetros.\n')
            print(uso_evaluar_aleatorio)
            exit()
        dataset_name = sys.argv[2]
        if dataset_name not in ['iris', 'covtype']:
            print('Error. Nombre de dataset incorrecto. Solo puede ser "iris" o "covtype"\n')
            print(uso_evaluar_aleatorio)
            exit()
        validation_precentage = float(sys.argv[3])
        if validation_precentage <= 0 or validation_precentage > 1:
            print('Error. Valor de proporción de instancias de validación' +
                  ' incorrecto. Solo puede ser un numero entre 0 y 1, 1 inclusive (e.g. 0.8)\n')
            print(uso_evaluar_aleatorio)
            exit()
        output_file = sys.argv[4]
        if os.path.isfile(output_file):
            print('Error. Ya existe el archivo especificado o no es un nombre válido de archivo.\n')
            print(uso_evaluar_aleatorio)
            exit()

        print('Leyendo conjunto de instancias\n')
        data = Data.Data(dataset_name)
        print('Tomando el subconjunto de validación\n')
        _, data_validation = data.divide_corpus(1.0 - validation_precentage)
        print('Clasificando instancias con el clasificador aleatorio\n')
        classification = Classifier.classify_dataset_random(data_validation)
        print('Evaluando clasficador\n')
        print('Guardando métricas en {file}'.format(file=output_file))
        classes = []
        for c in data_validation.classes:
            classes.append((str(c)))
        Evaluator.evaluate_classificator(classification, classes,
                                         data_validation.dataset, len(data_validation.dataset),
                                         output_file)
        exit()
    else:
        print('Error. Modo de uso inválido. Los posibles modos de uso son Entrenar y Evaluar\n')
        print(uso_general + uso_entrenar + uso_evaluar + uso_evaluar_aleatorio)
        exit()

import sys
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.cross_validation import StratifiedShuffleSplit
import itertools

dataset = sys.argv[1]

# Read the data set into memory
input_data = pd.read_csv(dataset, compression='gzip', sep='\t')

for (C, loss, max_iter) in itertools.product([0.01, 0.1, 0.5, 1.0, 10.0, 50.0, 100.0],
                                             ['hinge', 'squared_hinge'],
                                             [10, 100, 500, 1000, 2000]):
    for dataset_repeat in range(1, 31):
        # Divide the data set into a training and testing sets, each time with a different RNG seed
        training_indices, testing_indices = next(iter(StratifiedShuffleSplit(input_data['class'].values,
                                                                             n_iter=1,
                                                                             train_size=0.75,
                                                                             test_size=0.25,
                                                                             random_state=dataset_repeat)))
    
        training_features = input_data.loc[training_indices].drop('class', axis=1).values
        training_classes = input_data.loc[training_indices, 'class'].values
    
        testing_features = input_data.loc[testing_indices].drop('class', axis=1).values
        testing_classes = input_data.loc[testing_indices, 'class'].values
    
        # Create and fit the model on the training data
        try:
            clf = LinearSVC(C=C, loss=loss, max_iter=max_iter)
            clf.fit(training_features, training_classes)
            testing_score = clf.score(testing_features, testing_classes)
        except:
            continue
    
        param_string = ''
        param_string += 'C={},'.format(C)
        param_string += 'loss={},'.format(loss)
        param_string += 'max_iter={}'.format(max_iter)
    
        out_text = '\t'.join([dataset.split('/')[-1][:-7],
                              'LinearSVC',
                              param_string,
                              str(testing_score)])
    
        print(out_text)

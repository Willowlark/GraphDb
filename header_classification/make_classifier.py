import os
import pickle
import random

from Mark1 import nltk
from csv_read import exe_read
from feature_extraction import extract_features

pickled_classifier_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources', 'pickled_classifier')
local_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv', 'input.csv')


class classifier_factory():
    """
    This class holds the necessary operations to build and store a trained nltk.NaiveBayesClassifier
    The classifier can be returned in active state for, or serialized and written to a specified file for storage.
    """

    def __init__(self, *input_files):
        """
        Constructor for classifier_factory, takes 0 or more input files to be processed

        `param input_files`: the file path names to files to be used for training.
        """
        self.input_files = input_files

    def make_classifier(self, training_data=None, out_file=None, shuffle=True):
        """
        This method fabricates the goal classifier object.

        NOTE: is outfile is None, the classifier object created is returned, else it is written the specified location

        `param training_data`: optional, pre-constructed training data to be used for training.
        `param out_file`: optional, file path name to destination of pickles classifier NOTE if none, classifier object will be returned by this procedure
        `param shuffle`: optional, shuffle data before training for improved quality classifier
        `return`: None or object nltk.NaiveBayesClassifier constructed.
        """

        if training_data is None:
            input_training_data = []
            for file in self.input_files:
                input_training_data.extend(exe_read(file))
        else:
            input_training_data = training_data

        if shuffle:
            # Shuffle data to ensure improved approximation for training
            random.shuffle(input_training_data)

        train_set = [(extract_features(n), _class) for (n, _class) in input_training_data]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        if out_file is None:
            return classifier
        with open(out_file, 'wb') as fileObject:
            pickle.dump(classifier,fileObject)
        print 'Classifier Created Successfully. Pickled in file:', out_file

if __name__ == '__main__':
    """Execute Script"""
    factory = classifier_factory(local_file_path)
    factory.make_classifier(out_file=pickled_classifier_path)
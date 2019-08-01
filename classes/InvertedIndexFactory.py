import io
import re
import os
import hashedindex
import numpy as np
from os import listdir
from os.path import isfile, join
from hashedindex import textparser
import multiprocessing as mp


class InvertedIndexClass:
    def __init__(self, location=None, filename=None):
        if location is not None and filename is not None:
            self.dir = re.sub('((\/|\\\)?(\.\.))+', "", location)
            self.env_dir = os.path.join(os.path.dirname(__file__), re.sub(self.dir, "", location))
            self.collection = filename

        else:
            self.dir = "/input/"
            self.env_dir = os.path.join(os.path.dirname(__file__), '..')

        self.docnames = []
        self.terms = []
        self.matrix = []

        # Adding these values in order to multi-process read lines implementation
        self.core_counter = 4
        self.index = hashedindex.HashedIndex()

    def get_data_from_input(self):
        if os.path.exists(self.env_dir + self.dir) and len(os.listdir(self.env_dir + self.dir)) > 0:
            self.docnames = [f for f in listdir(self.env_dir + self.dir) if isfile(join(self.env_dir + self.dir, f))]

            for doc in self.docnames:
                with io.open(self.env_dir + self.dir + doc, 'r', encoding='utf8') as fp:
                    text = re.sub('(\t\n|\t|\n|_)', " ", fp.read())

                    for term in textparser.word_tokenize(text, min_length=2, ignore_numeric=True):
                        self.index.add_term_occurrence(term, doc)

            # Esto es una PoC para ver si es que se genera efectivamente una matriz de 1's y 0's con las incidencias
            for doc in self.docnames:
                aux_doc = []
                for term in self.index.terms():
                    if round(self.index.get_term_frequency(term, doc)) > 0:
                        aux_doc.append(1)
                    else:
                        aux_doc.append(0)

                self.matrix.append(aux_doc)

            self.matrix = np.matrix(self.matrix)

            # Esto es para crear el array de términos
            for term in self.index.terms():
                self.terms.append(re.sub("(\(\'|\'\,\))", "", str(term)))

        else:
            print("Attempting to create '{}' into {}.".format(self.dir, self.env_dir))

            if not os.path.exists(self.env_dir + self.dir):
                os.mkdir(self.env_dir + self.dir, mode=777)
                print("The input folder, '{}', was created successfully in {}.".format(self.dir, self.env_dir))

            else:
                print("The input folder, '{}', is empty in {}.".format(self.dir, self.env_dir))

        return self.matrix, self.docnames, self.terms

    def get_data_from_collection(self):
        if os.path.exists(self.env_dir + self.dir) and len(os.listdir(self.env_dir + self.dir)) > 0 and len(self.collection) > 0:
            index = hashedindex.HashedIndex()
            doc_count = 0

            with io.open(self.env_dir + self.dir + self.collection, 'r', encoding='utf8') as fp:
                print("File {} is successfully opened.".format(self.collection))

            # Esto es una PoC para ver si es que se genera efectivamente una matriz de 1's y 0's con las incidencias
            print("Reading collection - Before")
            for line in fp:
                print("Reading a line - Before")
                for term in textparser.word_tokenize(line, min_length=2, ignore_numeric=True):
                    print("Tokenizing {} - Adding".format(term))
                    index.add_term_occurrence(term, self.collection + "/line-" + str(doc_count))
                    print("Tokenizing {} - END".format(term)) 

                self.docnames.append(self.collection + "/line-" + str(doc_count))
                print("Reading a line - After")
  
                doc_count = doc_count + 1
            print("Reading collection - Before")
            for doc in self.docnames:
                aux_doc = []
                for term in index.terms():
                    if round(index.get_term_frequency(term, doc)) > 0:
                        aux_doc.append(1)
                    else:
                        aux_doc.append(0)

                self.matrix.append(aux_doc)

            self.matrix = np.matrix(self.matrix)

            # Esto es para crear el array de términos
            for term in index.terms():
                self.terms.append(re.sub("(\(\'|\'\,\))", "", str(term)))

        else:
            print("Attempting to create '{}' into {}.".format(self.dir, self.env_dir))

            if not os.path.exists(self.env_dir + self.dir):
                os.mkdir(self.env_dir + self.dir, mode=777)
                print("The input folder, '{}', was created successfully in {}.".format(self.dir, self.env_dir))

            else:
                print("The input folder, '{}', is empty in {}.".format(self.dir, self.env_dir))

        return self.matrix, self.docnames, self.terms

    ''' OLD IMPLEMENTATION - For archiving purposes    
        def get_data_from_collection(self):
            if os.path.exists(self.env_dir + self.dir) and len(os.listdir(self.env_dir + self.dir)) > 0 and len(self.collection) > 0:
                index = hashedindex.HashedIndex()
                doc_count = 0

                with io.open(self.env_dir + self.dir + self.collection, 'r', encoding='utf8') as fp:
                    for line in fp.readlines():
                        print(line)
                        for term in textparser.word_tokenize(line, min_length=2, ignore_numeric=True):
                            index.add_term_occurrence(term, self.collection + "/line-" + str(doc_count))

                        self.docnames.append(self.collection + "/line-" + str(doc_count))

                        doc_count = doc_count + 1

                # Esto es una PoC para ver si es que se genera efectivamente una matriz de 1's y 0's con las incidencias
                for doc in self.docnames:
                    aux_doc = []
                    for term in index.terms():
                        if round(index.get_term_frequency(term, doc)) > 0:
                            aux_doc.append(1)
                        else:
                            aux_doc.append(0)

                    self.matrix.append(aux_doc)

                self.matrix = np.matrix(self.matrix)

                # Esto es para crear el array de términos
                for term in index.terms():
                    self.terms.append(re.sub("(\(\'|\'\,\))", "", str(term)))

            else:
                print("Attempting to create '{}' into {}.".format(self.dir, self.env_dir))

                if not os.path.exists(self.env_dir + self.dir):
                    os.mkdir(self.env_dir + self.dir, mode=777)
                    print("The input folder, '{}', was created successfully in {}.".format(self.dir, self.env_dir))

                else:
                    print("The input folder, '{}', is empty in {}.".format(self.dir, self.env_dir))

            return self.matrix, self.docnames, self.terms'''

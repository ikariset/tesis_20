import io
import re
import os
from os import listdir
from os.path import isfile, join
import hashedindex
import numpy as np

from hashedindex import textparser


class InvertedIndexClass:
    def __init__(self):
        self.dir = "/input/"
        self.env_dir = os.path.join(os.path.dirname(__file__), '..')
        self.docnames = []
        self.terms = []
        self.matrix = []

    def get_data_from_input(self):
        if os.path.exists(self.env_dir + self.dir) and len(os.listdir(self.env_dir + self.dir)) > 0:
            self.docnames = [f for f in listdir(self.env_dir + self.dir) if isfile(join(self.env_dir + self.dir, f))]
            index = hashedindex.HashedIndex()

            for doc in self.docnames:
                with io.open(self.env_dir + self.dir + doc, 'r', encoding='utf8') as fp:
                    text = re.sub('(\t\n|\t|\n|_)', " ", fp.read())

                    for term in textparser.word_tokenize(text, min_length=2, ignore_numeric=True):
                        index.add_term_occurrence(term, doc)

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

        return self.matrix, self.docnames, self.terms

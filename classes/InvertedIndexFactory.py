<<<<<<< HEAD
import io
import re
import os
import hashedindex
import numpy as np
import time
=======
import io, re, os, psutil, hashedindex
import logging as lg
import numpy as np
>>>>>>> 70ef5b9eea74b7636d21763203a66738619c81cf
from os import listdir
from os.path import isfile, join
from hashedindex import textparser
import classes.SignalWatchdog
from classes.SignalWatchdog import SignalWatchdog


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
        self.index = hashedindex.HashedIndex()

        # PoC -- Trying to bypass this issue in order to get more memory.

        # self._signals = SignalWatchdog()
        self._exception_val = 'OK'
        self._exception_message = 'All is OK in my fields'
        self._log_delta_lines = 1000
        io.open("../processing_log.txt", 'w+', encoding='utf8').close()
        lg.basicConfig(filename="../processing_log.txt", level=lg.INFO,
                       format="%(asctime)s -- STATUS: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


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

    def map(self):
        try:
            # Esto es una PoC para ver si es que se genera efectivamente una matriz de 1's y 0's con las incidencias
            with io.open(self.env_dir + self.dir + self.collection, 'r', encoding='utf8') as fp:
                lg.info("File {} is successfully opened.\n".format(self.collection))
                line_count = self._log_delta_lines
                doc_count = 1
                aux_line = ""
                io.open("../indexes/docs_index.txt", 'w+', encoding='utf8').close()
                io.open("../indexes/map_index.txt", 'w+', encoding='utf8').close()
                docs_index = io.open("../indexes/docs_index.txt", 'w+', encoding='utf8')
                map_index = io.open("../indexes/map_index.txt", 'w+', encoding='utf8')

                for line in fp:
                    # print("Reading a line - Before")
                    aux_doc = self.collection + "/line-" + str(doc_count)
                    docs_index.writelines(aux_doc + "\n")
                    for term in textparser.word_tokenize(line, min_length=2, ignore_numeric=True):
                        aux_line = str(term) + ", " + aux_doc
                        map_index.writelines(aux_line + "\n")

                    if line_count == self._log_delta_lines:
                        lg.info("Finishing read line {}\nCPU: {}\nRAM: {}".format(
                            doc_count,
                            psutil.cpu_stats(),
                            psutil.virtual_memory()))
                        lg.info(
                            '------------------------------------------------------------------------------------\n')
                        line_count = 1
                    else:
                        line_count += 1

                    doc_count = doc_count + 1

            lg.info("Status: Indexing Complete\nCPU: {}\nRAM: {}".format(
                psutil.cpu_stats(),
                psutil.virtual_memory()))
            lg.info('------------------------------------------------------------------------------------\n')

        except Exception as exc:
            self._exception_val = type(exc).__name__
            self._exception_message = str(exc)

        finally:
            lg.warning(
                "Closing the process with following status\nException Name: {}\nException Message: {}\nCPU: {}\nRAM: {}".format(
                    self._exception_val,
                    self._exception_message,
                    psutil.cpu_stats(),
                    psutil.virtual_memory()))
            lg.warning('------------------------------------------------------------------------------------\n')

    def get_data_from_collection(self):
        if os.path.exists(self.env_dir + self.dir) and len(os.listdir(self.env_dir + self.dir)) > 0 and len(
                self.collection) > 0:
            doc_count = 0
            log_delta_lines = 1000

            try:
                # Esto es una PoC para ver si es que se genera efectivamente una matriz de 1's y 0's con las incidencias
                with io.open(self.env_dir + self.dir + self.collection, 'r', encoding='utf8') as fp:
                    lg.info("File {} is successfully opened.\n".format(self.collection))
                    line_count = log_delta_lines
                    for line in fp:
                        # print("Reading a line - Before")
                        for term in textparser.word_tokenize(line, min_length=2, ignore_numeric=True):
                            self.index.add_term_occurrence(term, self.collection + "/line-" + str(doc_count))

                        self.docnames.append(self.collection + "/line-" + str(doc_count))
                        if line_count == log_delta_lines:
                            lg.info("Finishing read line {}\nCPU: {}\nRAM: {}".format(
                                doc_count,
                                psutil.cpu_stats(),
                                psutil.virtual_memory()))
                            lg.info(
                                '------------------------------------------------------------------------------------\n')
                            line_count = 1
                        else:
                            line_count += 1

                        doc_count = doc_count + 1

                lg.info("Status: Indexing Complete\nCPU: {}\nRAM: {}".format(
                    psutil.cpu_stats(),
                    psutil.virtual_memory()))
                lg.info('------------------------------------------------------------------------------------\n')

                line_count = log_delta_lines

                for doc in self.docnames:
                    aux_doc = []
                    for term in self.index.terms():
                        if round(self.index.get_term_frequency(term, doc)) > 0:
                            aux_doc.append(1)
                        else:
                            aux_doc.append(0)

                    self.matrix.append(aux_doc)

                    if line_count == log_delta_lines:
                        lg.info("Occurrence Array Generation for a doc\nCPU: {}\nRAM: {}".format(
                            psutil.cpu_stats(),
                            psutil.virtual_memory()))
                        lg.info(
                            '------------------------------------------------------------------------------------\n')
                        line_count = 1

                    else:
                        line_count += 1

                self.matrix = np.matrix(self.matrix)

                lg.info("Status: Occurrence Matrix complete\nCPU: {}\nRAM: {}".format(
                    psutil.cpu_stats(),
                    psutil.virtual_memory()))
                lg.info('------------------------------------------------------------------------------------\n')

                # Esto es para crear el array de términos
                for term in self.index.terms():
                    self.terms.append(re.sub("(\(\'|\'\,\))", "", str(term)))

                lg.info("Status: Finishing all process\nCPU: {}\nRAM: {}".format(
                    psutil.cpu_stats(),
                    psutil.virtual_memory()))
                lg.info('------------------------------------------------------------------------------------\n')

            except Exception as exc:
                self._exception_val = type(exc).__name__
                self._exception_message = str(exc)

            finally:
                lg.warning(
                    "Closing the process with following status\nException Name: {}\nException Message: {}\nCPU: {}\nRAM: {}".format(
                        self._exception_val,
                        self._exception_message,
                        psutil.cpu_stats(),
                        psutil.virtual_memory()))
                lg.warning('------------------------------------------------------------------------------------\n')

        else:
            print("Attempting to create '{}' into {}.".format(self.dir, self.env_dir))

            if not os.path.exists(self.env_dir + self.dir):
                os.mkdir(self.env_dir + self.dir, mode=777)
                print("The input folder, '{}', was created successfully in {}.".format(self.dir, self.env_dir))

            else:
                print("The input folder, '{}', is empty in {}.".format(self.dir, self.env_dir))

        return self.matrix, self.docnames, self.terms

    '''
    This function was the last one before Map-Reduce shit
    def get_data_from_collection(self):
        if os.path.exists(self.env_dir + self.dir) and len(os.listdir(self.env_dir + self.dir)) > 0 and len(
                self.collection) > 0:
            doc_count = 0
            log_delta_lines = 1000

            try:
                # Esto es una PoC para ver si es que se genera efectivamente una matriz de 1's y 0's con las incidencias
                with io.open(self.env_dir + self.dir + self.collection, 'r', encoding='utf8') as fp:
                    lg.info("File {} is successfully opened.\n".format(self.collection))
                    line_count = log_delta_lines
                    for line in fp:
                        # print("Reading a line - Before")
                        for term in textparser.word_tokenize(line, min_length=2, ignore_numeric=True):
                            self.index.add_term_occurrence(term, self.collection + "/line-" + str(doc_count))

                        self.docnames.append(self.collection + "/line-" + str(doc_count))
                        if line_count == log_delta_lines:
                            lg.info("Finishing read line {}\nCPU: {}\nRAM: {}".format(
                                doc_count,
                                psutil.cpu_stats(),
                                psutil.virtual_memory()))
                            lg.info(
                                '------------------------------------------------------------------------------------\n')
                            line_count = 1
                        else:
                            line_count += 1

                        doc_count = doc_count + 1

                lg.info("Status: Indexing Complete\nCPU: {}\nRAM: {}".format(
                    psutil.cpu_stats(),
                    psutil.virtual_memory()))
                lg.info('------------------------------------------------------------------------------------\n')

                line_count = log_delta_lines

                for doc in self.docnames:
                    aux_doc = []
                    for term in self.index.terms():
                        if round(self.index.get_term_frequency(term, doc)) > 0:
                            aux_doc.append(1)
                        else:
                            aux_doc.append(0)

                    self.matrix.append(aux_doc)

                    if line_count == log_delta_lines:
                        lg.info("Occurrence Array Generation for a doc\nCPU: {}\nRAM: {}".format(
                            psutil.cpu_stats(),
                            psutil.virtual_memory()))
                        lg.info(
                            '------------------------------------------------------------------------------------\n')
                        line_count = 1

                    else:
                        line_count += 1

                self.matrix = np.matrix(self.matrix)

                lg.info("Status: Occurrence Matrix complete\nCPU: {}\nRAM: {}".format(
                    psutil.cpu_stats(),
                    psutil.virtual_memory()))
                lg.info('------------------------------------------------------------------------------------\n')

                # Esto es para crear el array de términos
                for term in self.index.terms():
                    self.terms.append(re.sub("(\(\'|\'\,\))", "", str(term)))

                lg.info("Status: Finishing all process\nCPU: {}\nRAM: {}".format(
                    psutil.cpu_stats(),
                    psutil.virtual_memory()))
                lg.info('------------------------------------------------------------------------------------\n')

            except Exception as exc:
                self._exception_val = type(exc).__name__
                self._exception_message = str(exc)

            finally:
                lg.warning(
                    "Closing the process with following status\nException Name: {}\nException Message: {}\nCPU: {}\nRAM: {}".format(
                        self._exception_val,
                        self._exception_message,
                        psutil.cpu_stats(),
                        psutil.virtual_memory()))
                lg.warning('------------------------------------------------------------------------------------\n')

        else:
            print("Attempting to create '{}' into {}.".format(self.dir, self.env_dir))

            if not os.path.exists(self.env_dir + self.dir):
                os.mkdir(self.env_dir + self.dir, mode=777)
                print("The input folder, '{}', was created successfully in {}.".format(self.dir, self.env_dir))

            else:
                print("The input folder, '{}', is empty in {}.".format(self.dir, self.env_dir))

        return self.matrix, self.docnames, self.terms'''

    def store_hashedindex(self):
        '''Tengo que hacer cada vez que se reciba una señal de término, que los archivos se guarden en un
        archivo de caché'''
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

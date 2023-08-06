import time
import numpy as np
from scipy.io import arff


class FileReader:

    @staticmethod
    def read_file(fileName, has_header=True, labelLastColumn=True, separator=","):
        file = fileName.split(".")[1]
        if file == "arff" or file == "ts":
            return FileReader.load_arff_data(fileName)
        return FileReader.readCSVToListDataset(fileName, has_header, labelLastColumn, False, separator)

    @staticmethod
    def load_data(full_data_path):
        f = open(full_data_path)
        print("FICHERO:", f)
        data, meta = arff.loadarff(f)
        f.close()
        return data

    @staticmethod
    def load_arff_data(fullpath):
        try:
            file = FileReader.load_data(fullpath)
            print("Reading File: [", fullpath, "]")
        except:
            print("File Not Found: [", fullpath, "]")
            return
        start = time.time()
        dataset = list()
        labels = list()
        tam_series = len(file)
        for i in range(0, tam_series):
            serie_lenth = len(file[i])
            if serie_lenth <= 0:
                continue
            try:
                class_label = int(file[i][serie_lenth - 1])
            except:
                class_label = file[i][serie_lenth - 1]
            serie = list()
            for j in range(0, serie_lenth - 1):
                try:
                    serie.append(np.double(file[i][j]))
                except:
                    continue
            serie = np.asarray(serie)
            dataset.append(serie)
            labels.append(class_label)
        end = time.time()
        elapsed = end - start
        print("finished in", elapsed, "seconds")
        return dataset, labels

    @staticmethod
    def parse_arff_data(file):
        start = time.time()
        dataset = list()
        labels = list()
        tam_series = len(file)
        for i in range(0, tam_series):
            serie_lenth = len(file[i])
            if serie_lenth <= 0:
                continue
            try:
                class_label = int(file[i][serie_lenth - 1])
            except:
                class_label = file[i][serie_lenth - 1]
            serie = list()
            for j in range(0, serie_lenth - 1):
                try:
                    serie.append(np.double(file[i][j]))
                except:
                    continue
            dataset.append(serie)
            labels.append(class_label)
        end = time.time()
        elapsed = end - start
        print("finished in", elapsed, "seconds")
        return dataset, labels

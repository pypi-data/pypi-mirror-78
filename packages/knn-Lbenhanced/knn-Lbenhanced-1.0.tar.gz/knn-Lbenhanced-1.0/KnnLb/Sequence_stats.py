import sys
import math
import numpy as np


class Tuple:
    def __init__(self, first=0, second=0):
        self.first = first
        self.second = second

    def set_fist(self, first):
        self.first = first

    def set_second(self, second):
        self.second = second

    pass


class SequenceStats:

    def __init__(self, dataset=None, window=0):
        self.n_seq = len(dataset)
        self.seq_len = len(dataset[0])

        self.upper_envelope = np.zeros([self.n_seq, self.seq_len])
        self.lower_envelope = np.zeros([self.n_seq, self.seq_len])
        self.upper_rear_envelope = np.zeros([self.n_seq, self.seq_len])
        self.lower_rear_envelope = np.zeros([self.n_seq, self.seq_len])
        self.upper_front_envelope = np.zeros([self.n_seq, self.seq_len])
        self.lower_front_envelope = np.zeros([self.n_seq, self.seq_len])

        self.sorted_sequence = np.zeros([self.n_seq, self.seq_len, self.seq_len])
        self.first_3sorted = np.zeros([self.n_seq, 3])
        self.last_3sorted = np.zeros([self.n_seq, 3])

        self.dataset = dataset
        self.mins = np.zeros([self.n_seq])
        self.maxs = np.zeros([self.n_seq])
        self.index_mins = np.zeros([self.n_seq])
        self.index_maxs = np.zeros([self.n_seq])
        self.is_min_first = np.zeros([self.n_seq])
        self.is_min_last = np.zeros([self.n_seq])
        self.is_max_first = np.zeros([self.n_seq])
        self.is_max_last = np.zeros([self.n_seq])
        self.indices_sorted = np.zeros([self.n_seq, self.seq_len, 2])
        # self.indices_sorted = [[Tuple() for i in range(self.n_seq)] for j in range(self.seq_len)]

        for i in range(0, len(self.dataset)):
            minimum = sys.float_info.min
            maximum = sys.float_info.max
            index_min = -1
            index_max = -1

            for j in range(0, len(self.dataset[i])):

                elt = dataset[i][j]
                if elt > maximum:
                    maximum = elt
                    index_max = j
                if elt < minimum:
                    minimum = elt
                    index_min = j
                tuple = Tuple(j, abs(elt))
                self.indices_sorted[i][j][0] = j
                self.indices_sorted[i][j][1] = abs(elt)
            self.index_maxs[i] = index_max
            self.index_mins[i] = index_min
            self.mins[i] = minimum
            self.maxs[i] = maximum
            self.is_min_first[i] = (index_min == 0)
            self.is_min_last[i] = (index_min == (len(self.dataset[i]) - 2))
            self.is_max_first[i] = (index_max == 0)
            self.is_max_last[i] = (index_max == (len(self.dataset[i]) - 2))
            # self.indices_sorted = np.sort(self,)
            # self.indices_sorted = np.sort(self.indices_sorted)
        self.indices_sorted = np.sort(self.indices_sorted)[::-1]
        self.set_all_envelopes(window)

    def set_dataset(self, dt):
        self.__init__(dt)

    def set_all_envelopes(self, window):
        for index in range(0, self.n_seq):
            sequence = self.dataset[index]
            length = len(sequence)
            for i in range(0, length):
                minimo = math.inf
                maximo = -math.inf
                min_rear = math.inf
                max_rear = -math.inf
                min_front = math.inf
                max_front = -math.inf
                start_w = max(0, i - window)
                stop_w = min(length - 1, i + window)
                j = start_w
                while j <= stop_w:
                    value = sequence[j]
                    minimo = min(minimo, value)
                    maximo = max(maximo, value)
                    if j <= i:
                        min_rear = min(min_rear, value)
                        max_rear = max(max_rear, value)
                    if j >= i:
                        min_front = min(min_front, value)
                        max_front = max(max_front, value)
                    j = j + 1
                self.lower_envelope[index][i] = minimo
                self.upper_envelope[index][i] = maximo
                self.lower_rear_envelope[index][i] = min_rear
                self.upper_rear_envelope[index][i] = max_rear
                self.lower_front_envelope[index][i] = min_front
                self.upper_front_envelope[index][i] = max_front

    def init_keogh(self, dataset):
        self.n_seq = dataset.num_instances()
        self.seq_len = dataset.get_instance(0).num_series()
        self.upper_envelope = np.array([self.n_seq, self.seq_len])
        self.lower_envelope = np.array([self.n_seq, self.seq_len])
        self.dataset = dataset

    def is_min_first(self, i):
        return self.is_min_first[i]

    def is_max_first(self, i):
        return self.is_max_first[i]

    def is_min_last(self, i):
        return self.is_min_last[i]

    def is_max_last(self, i):
        return self.is_max_last[i]

    def get_min(self, i):
        return self.mins[i]

    def get_max(self, i):
        return self.maxs[i]

    def get_index_with_highestval(self, i, n):
        return self.indices_sorted[i][n][0]

    def get_upper_envelope(self, i, j):
        return self.upper_envelope[i][j]

    def get_upper_front_envelope(self, i, j):
        return self.upper_envelope[i][j]

    def get_upper_rear_envelope(self, i, j):
        return self.upper_rear_envelope[i][j]

    def get_lower_envelope(self, i, j):
        return self.lower_envelope[i][j]

    def get_lower_front_envelope(self, i, j):
        return self.lower_rear_envelope[i][j]

    def get_lower_rear_envelope(self, i, j):
        return self.lower_rear_envelope[i][j]

    pass

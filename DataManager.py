#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scipy.io as sio
import numpy as np
general_file_keys = ['__version__', '__header__', '__globals__']


class DataObject:
    def __init__(self, file):
        self.mat_file = file
        self._mat_contents = sio.loadmat(self.mat_file)
        self.data_titles = self.__data_titles__()
        self.data_mean = {}
        self.__data_mean__()

    def __data_titles__(self):
        titles = []
        for key in self._mat_contents.keys():
            if not any((True for x in general_file_keys if x == key)):
                titles.append(key)
        return titles

    def __data_mean__(self):
        for key in self.get_titles():
            temp = np.array(self._mat_contents.get(key))
            # Compute the mean in the 3 dimension
            # Mean in all the samples
            mean = np.mean(temp, axis=2)
            self.data_mean[key] = mean

    def get_titles(self):
        return self.data_titles

    def get_sample(self, key):
        return self.data_mean.get(key)


class PolarConverter:
    def __init__(self, data, x_range=60, y_min=0.2):
        self.sample_data = data
        self.sample_x_range = x_range
        self.sample_y_min = y_min

    def set_parameters(self, x_range, y_min):
        self.sample_x_range = x_range
        self.sample_y_min = y_min

    @staticmethod
    def read_in_chunks(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    def create_dataset(self):
        amplitude = []
        n = np.ceil(len(self.sample_data)/self.sample_x_range)
        for chunk in self.read_in_chunks(self.sample_data, self.sample_x_range):
            amplitude.append(np.mean(chunk))
        return n, amplitude

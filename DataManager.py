#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scipy.io as sio
import numpy as np
general_file_keys = ['__version__', '__header__', '__globals__']

COLOR_RED = [1, 0, 0]
COLOR_BLUE = [0, 0, 1]


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

    def get_shape_by_key(self, key):
        return np.shape(self.data_mean.get(key))

    @staticmethod
    def get_shape(data):
        return np.shape(data)


class PolarConverter:
    def __init__(self, x_range=60, y_min=0.2):
        self.sample_x_range = x_range
        self.sample_y_min = y_min

    def set_parameters(self, x_range, y_min):
        self.sample_x_range = x_range
        self.sample_y_min = y_min

    @staticmethod
    def read_in_chunks(seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    # Create a mean per range data set, like a bar set of the data
    def polar_scatter_conversion(self, data):
        amplitude = []
        time = []
        color = []
        n = 0
        for chunk in self.read_in_chunks(data, self.sample_x_range):
            amp_value = np.mean(chunk)
            if abs(amp_value) < self.sample_y_min:
                n += 1
                continue

            amplitude.append(amp_value)
            n += 1
            time.append((n-1)*self.sample_x_range + self.sample_x_range/2.0)

            if amp_value >= 0:
                color.append(COLOR_BLUE)
            else:
                color.append(COLOR_RED)

        # Return a Normalized absolute amplitude
        return time, amplitude, color

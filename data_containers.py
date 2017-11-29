import scipy.io as sio
import numpy as np
import numpy.linalg as npla
import configparser
import argparse
import itertools
import copy


class DetectionPoint(object):
    def __init__(self, mcc=0, beam=0, rng=0.0,
                 vel=0.0, az=0.0):

        self._y_correction_dir = -1 if left else 1
        self._mcc = mcc
        self._beam = beam
        self._rng = rng
        self._vel = vel
        self._az = az
        self._x = self._rng * np.cos(self._az)
        self._y = self._y_correction_dir * (self._rng * np.sin(self._az) + car_width / 2)


class DetectionList(list):
    def __init__(self):
        super().__init__()
        self._y_minmax = (0, 0)
        self._x_minmax = (0, 0)
        self._az_minmax = (0, 0)
        self._vel_minmax = (0, 0)
        self._rng_minmax = (0, 0)
        self._mcc_minmax = (0, 0)

    def __iter__(self):
        return


    def append_detection(self, detection_point):
        self.append(detection_point)
        self._y_minmax = (min([elem._y for elem in self]), max([elem._y for elem in self]))
        self._x_minmax = (min([elem._x for elem in self]), max([elem._x for elem in self]))
        self._az_minmax = (min([elem._az for elem in self]), max([elem._az for elem in self]))
        self._vel_minmax = (min([elem._vel for elem in self]), max([elem._vel for elem in self]))
        self._rng_minmax = (min([elem._rng for elem in self]), max([elem._rng for elem in self]))
        self._mcc_minmax = (min([elem._mcc for elem in self]), max([elem._mcc for elem in self]))

    def append_data_from_csv(self,filename):
        data = None
        return data

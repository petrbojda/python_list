import scipy.io as sio
import numpy as np
import numpy.linalg as npla
import configparser
import argparse
import itertools
import copy
import csv

class DetectionPoint(object):
    def __init__(self, mcc=0, x=0.0, y=0.0,
                 vel=0.0, az=0.0, rng=0.0):
        self._mcc = mcc
        self._vel = vel
        self._x = x
        self._y = y
        self._az = az
        self._rng = rng

class DetectionList(list):
    def __init__(self):
        super().__init__()
        self._y_minmax = (0, 0)
        self._x_minmax = (0, 0)
        self._az_minmax = (0, 0)
        self._vel_minmax = (0, 0)
        self._rng_minmax = (0, 0)
        self._mcc_minmax = (0, 0)

    def append_detection(self, detection_point):
        self.append(detection_point)
        self._y_minmax = (min([elem._x for elem in self]), max([elem._x for elem in self]))
        self._x_minmax = (min([elem._y for elem in self]), max([elem._y for elem in self]))
        self._az_minmax = (min([elem._az for elem in self]), max([elem._az for elem in self]))
        self._vel_minmax = (min([elem._vel for elem in self]), max([elem._vel for elem in self]))
        self._rng_minmax = (min([elem._rng for elem in self]), max([elem._rng for elem in self]))
        self._mcc_minmax = (min([elem._mcc for elem in self]), max([elem._mcc for elem in self]))

    def append_data_from_csv(self,filename):
        with open (filename,newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print("dc: Appending data from a csv file: mcc",row['mcc'],"x",row['x'],"y",row['y'],"vel",row['vel'])
                self.append_detection(DetectionPoint(mcc=int(row['mcc']),
                                                     x=float(row['x']),
                                                     y=float(row['y']),
                                                     vel=float(row['vel']) ))
        data = None
        return data

    def get_min_mcc(self):
        return self._mcc_minmax[0]

    def get_max_mcc(self):
        return self._mcc_minmax[1]

def cnf_file_read(cnf_file):
        # Read the configuration file
        config = configparser.ConfigParser()
        config.read(cnf_file)  # "./setup.cnf"

        # Get a path to a folder with data
        conf_data = {"datafile": config.get('Datasets', 'data_01')}
        return conf_data

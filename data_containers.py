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
                 rvel=0.0, raz=0.0, rrng=0.0):
        self._mcc = mcc
        self._rvel = rvel
        self._x = x
        self._y = y
        self._rho = raz
        self._theta = rrng

    def assign_XYvel (self,x,y,rvel):
        self._rvel = rvel
        self._x = x
        self._y = y

    def complete_rhotheta_from_cartesian (self):
        self._theta = np.arctan(self._y/self._x)
        self._rho = np.linalg.norm([self._x,self._y])

    def get_mcc(self):
        return self._mcc

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_rvel(self):
        return self._rvel

    def get_rho(self):
        return self._rho

    def get_theta(self):
        return self._theta

    def get_theta_deg(self):
        return self._theta *180/np.pi


class DetectionList(list):
    def __init__(self):
        super().__init__()
        self._y_minmax = (0, 0)
        self._x_minmax = (0, 0)
        self._theta_minmax = (0, 0)
        self._rvel_minmax = (0, 0)
        self._rho_minmax = (0, 0)
        self._mcc_minmax = (0, 0)

        self._y_minmax_iter = (0, 0)
        self._x_minmax_iter = (0, 0)
        self._theta_minmax_iter = (0, 0)
        self._rvel_minmax_iter = (0, 0)
        self._rho_minmax_iter = (0, 0)
        self._mcc_minmax_iter = (0, 0)

        self._count = 0
        # self._sel = self.copy()
        #
        # print("dc.__init__: identity of lists self and self._sel:", self is self._sel)
        # print("dc.__init__: equality of lists self and self._sel:", self == self._sel)
        # print("dc.__init__: type of self:", type(self), "length:", len(self))
        # print("dc.__init__: type of self._sel:", type(self._sel), "length:", len(self._sel))

    def __iter__(self):
        self._count = 0
        return self

    def __next__(self):
        if self:
            if self._count > len(self)-1:
                raise StopIteration
            else:
                self._count += 1
                if  (self._mcc_minmax_iter[0] <= self[self._count-1]._mcc <= self._mcc_minmax_iter[1] and
                     self._x_minmax_iter[0] <= self[self._count-1]._x <= self._x_minmax_iter[1] and
                     self._y_minmax[0] <= self[self._count-1]._y <= self._y_minmax[1] and
                     self._rho_minmax_iter[0] <= self[self._count-1]._rho <= self._rho_minmax_iter[1] and
                     self._theta_minmax_iter[0] <= self[self._count-1]._theta <= self._theta_minmax_iter[1] and
                     self._rvel_minmax_iter[0] <= self[self._count-1]._rvel <= self._rvel_minmax_iter[1]):
                    return self[self._count-1]
                # TODO: Constrains must be set properly before it starts iterating
                else:
                    pass
        else:
            raise StopIteration

    def modify_iteration(self,selection):
        # TODO: Restart minmax constrains when this function is being called repeatedly
        self._mcc_minmax_iter = selection['mcc_tp'] if selection['mcc_tp'] else self._mcc_minmax
        self._x_minmax_iter = selection['x_tp'] if selection['x_tp'] else self._x_minmax
        self._y_minmax_iter = selection['y_tp'] if selection['y_tp'] else self._y_minmax
        self._rho_minmax_iter = selection['rho_tp'] if selection['rho_tp'] else self._rho_minmax
        self._theta_minmax_iter = selection['theta_tp'] if selection['theta_tp'] else self._theta_minmax
        self._rvel_minmax_iter = selection['rvel_tp'] if selection['rvel_tp'] else self._rvel_minmax

        print("dc: modify_iteration called, minmax constrains: ")
        print("dc: mcc", self._mcc_minmax)
        print("dc: x", self._x_minmax)
        print("dc: y", self._y_minmax)
        print("dc: rho", self._rho_minmax)
        print("dc: theta", self._theta_minmax)
        print("dc: rvel", self._rvel_minmax)

        print("dc: modify_iteration called, minmax ITER constrains: ")
        print("dc: mcc", self._mcc_minmax_iter)
        print("dc: x", self._x_minmax_iter)
        print("dc: y", self._y_minmax_iter)
        print("dc: rho", self._rho_minmax_iter)
        print("dc: theta", self._theta_minmax_iter)
        print("dc: rvel", self._rvel_minmax_iter)

       # selected_list = [elem for elem in self if (self._mcc_minmax_iter[0] <= elem._mcc <= self._mcc_minmax_iter[1] and
       #                                         self._x_minmax_iter[0] <= elem._x <= self._x_minmax_iter[1] and
       #                                         self._y_minmax[0] <= elem._y <= self._y_minmax[1] and
       #                                         self._rho_minmax_iter[0] <= elem._rho <= self._rho_minmax_iter[1] and
       #                                         self._theta_minmax_iter[0] <= elem._theta <= self._theta_minmax_iter[1] and
       #                                         self._rvel_minmax_iter[0] <= elem._rvel <= self._rvel_minmax_iter[1])]

        # print("dc.modify_iteration: identity of lists self and self._sel:", self is self._sel)
        # print("dc.modify_iteration: equality of lists self and self._sel:", self == self._sel)
        # print("dc.modify_iteration: type of self:", type(self), "length:",len(self))
        # print("dc.modify_iteration: type of self._sel:", type(self._sel), "length:",len(self._sel))

    def get_array_mcc(self):
        return [elem._mcc for elem in self]

    def get_array_x(self):
        return [elem._x for elem in self]

    def get_array_y(self):
        return [elem._y for elem in self]

    def get_array_rvel(self):
        return [elem._rvel for elem in self]

    def get_array_rho(self):
        return [elem._rho for elem in self]

    def get_array_theta(self):
        return [elem._theta for elem in self]

    def get_array_theta_deg(self):
        return [elem._theta*180/np.pi for elem in self]

    def append_detection(self, detection_point):
        self.append(detection_point)

    def recalculate_minmax(self):
        self._x_minmax = (min([elem._x for elem in self]), max([elem._x for elem in self]))
        self._y_minmax = (min([elem._y for elem in self]), max([elem._y for elem in self]))
        self._theta_minmax = (min([elem._theta for elem in self]), max([elem._theta for elem in self]))
        self._rvel_minmax = (min([elem._rvel for elem in self]), max([elem._rvel for elem in self]))
        self._rho_minmax = (min([elem._rho for elem in self]), max([elem._rho for elem in self]))
        self._mcc_minmax = (min([elem._mcc for elem in self]), max([elem._mcc for elem in self]))
        print("dc: recalculate_minmax called, minmax constrains: ")
        print("dc: mcc", self._mcc_minmax)
        print("dc: x", self._x_minmax)
        print("dc: y", self._y_minmax)
        print("dc: rho", self._rho_minmax)
        print("dc: theta", self._theta_minmax)
        print("dc: rvel", self._rvel_minmax)

        print("dc: recalculate_minmax called, minmax ITER constrains: ")
        print("dc: mcc", self._mcc_minmax_iter)
        print("dc: x", self._x_minmax_iter)
        print("dc: y", self._y_minmax_iter)
        print("dc: rho", self._rho_minmax_iter)
        print("dc: theta", self._theta_minmax_iter)
        print("dc: rvel", self._rvel_minmax_iter)


    def append_data_from_csv(self,filename):
        with open(filename,newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.append_detection(DetectionPoint(mcc=int(row['mcc'])))
                self[-1].assign_XYvel(x=float(row['x']), y=float(row['y']), rvel=float(row['vel']))
                self[-1].complete_rhotheta_from_cartesian()
                print("dc.append_data_from_csv: length of the list:",len(self))
                print("dc.append_data_from_csv: last assigned detection:", self[-1]._x,self[-1]._y)
        print("dc.append_data_from_csv, mcc:", [elem._mcc for elem in self])
        self.recalculate_minmax()

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

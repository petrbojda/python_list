import numpy as np
import configparser
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

    def keys(self):
        class_keys = ['_mcc','_rho','_theta','_rvel','_x','_y']
        return class_keys


class DetectionList(list):
    def __init__(self):
        super().__init__()
        self._y_minmax = [0, 0]
        self._x_minmax = [0, 0]
        self._theta_minmax = [0, 0]
        self._rvel_minmax = [0, 0]
        self._rho_minmax = [0, 0]
        self._mcc_minmax = [0, 0]

        self._y_minmax_iter = [0, 0]
        self._x_minmax_iter = [0, 0]
        self._theta_minmax_iter = [0, 0]
        self._rvel_minmax_iter = [0, 0]
        self._rho_minmax_iter = [0, 0]
        self._mcc_minmax_iter = [0, 0]

        self._count = 0

    def __iter__(self):
        self._count = 0
        return self

    def __next__(self):
        if self:
            if self._count > len(self)-1:
                raise StopIteration
            else:
                self._count += 1
                while not(self.test_detection_to_select(self[self._count-1])):
                    self._count += 1
                return self[self._count-1]
        else:
            raise StopIteration

    def append_detection(self, detection_point):
        self.append(detection_point)

    def append_data_from_csv(self,filename):
        with open(filename,newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.append_detection(DetectionPoint(mcc=int(row['mcc'])))
                self[-1].assign_XYvel(x=float(row['x']), y=float(row['y']), rvel=float(row['vel']))
                self[-1].complete_rhotheta_from_cartesian()
                if len(self)==1:
                    self.assign_minmax(self[-1])
                    self.assign_minmax_iter(self[-1])
                else:
                    self.calculate_minmax(self[-1])
                    self.calculate_minmax_iter(self[-1])

    def assign_minmax(self,detection):
        self._mcc_minmax[0] = detection._mcc
        self._mcc_minmax[1] = detection._mcc
        self._x_minmax[0] = detection._x
        self._x_minmax[1] = detection._x
        self._y_minmax[0] = detection._y
        self._y_minmax[1] = detection._y
        self._rho_minmax[0] = detection._rho
        self._rho_minmax[1] = detection._rho
        self._theta_minmax[0] = detection._theta
        self._theta_minmax[1] = detection._theta
        self._rvel_minmax[0] = detection._rvel
        self._rvel_minmax[1] = detection._rvel

    def assign_minmax_iter(self,detection):
        self._mcc_minmax_iter[0] = detection._mcc
        self._mcc_minmax_iter[1] = detection._mcc
        self._x_minmax_iter[0] = detection._x
        self._x_minmax_iter[1] = detection._x
        self._y_minmax_iter[0] = detection._y
        self._y_minmax_iter[1] = detection._y
        self._rho_minmax_iter[0] = detection._rho
        self._rho_minmax_iter[1] = detection._rho
        self._theta_minmax_iter[0] = detection._theta
        self._theta_minmax_iter[1] = detection._theta
        self._rvel_minmax_iter[0] = detection._rvel
        self._rvel_minmax_iter[1] = detection._rvel

    def calculate_minmax(self,detection):
        self._mcc_minmax[0] = detection._mcc if detection._mcc < self._mcc_minmax[0] else self._mcc_minmax[0]
        self._mcc_minmax[1] = detection._mcc if detection._mcc > self._mcc_minmax[1] else self._mcc_minmax[1]
        self._x_minmax[0] = detection._x if detection._x < self._x_minmax[0] else self._x_minmax[0]
        self._x_minmax[1] = detection._x if detection._x > self._x_minmax[1] else self._x_minmax[1]
        self._y_minmax[0] = detection._y if detection._y < self._y_minmax[0] else self._y_minmax[0]
        self._y_minmax[1] = detection._y if detection._y > self._y_minmax[1] else self._y_minmax[1]
        self._rho_minmax[0] = detection._rho if detection._rho < self._rho_minmax[0] else self._rho_minmax[0]
        self._rho_minmax[1] = detection._rho if detection._rho > self._rho_minmax[1] else self._rho_minmax[1]
        self._theta_minmax[0] = detection._theta if detection._theta < self._theta_minmax[0] else self._theta_minmax[0]
        self._theta_minmax[1] = detection._theta if detection._theta > self._theta_minmax[1] else self._theta_minmax[1]
        self._rvel_minmax[0] = detection._rvel if detection._rvel < self._rvel_minmax[0] else self._rvel_minmax[0]
        self._rvel_minmax[1] = detection._rvel if detection._rvel > self._rvel_minmax[1] else self._rvel_minmax[1]

    def calculate_minmax_iter(self,detection):
        self._mcc_minmax_iter[0] = detection._mcc if detection._mcc < self._mcc_minmax_iter[0] else self._mcc_minmax_iter[0]
        self._mcc_minmax_iter[1] = detection._mcc if detection._mcc > self._mcc_minmax_iter[1] else self._mcc_minmax_iter[1]
        self._x_minmax_iter[0] = detection._x if detection._x < self._x_minmax_iter[0] else self._x_minmax_iter[0]
        self._x_minmax_iter[1] = detection._x if detection._x > self._x_minmax_iter[1] else self._x_minmax_iter[1]
        self._y_minmax_iter[0] = detection._y if detection._y < self._y_minmax_iter[0] else self._y_minmax_iter[0]
        self._y_minmax_iter[1] = detection._y if detection._y > self._y_minmax_iter[1] else self._y_minmax_iter[1]
        self._rho_minmax_iter[0] = detection._rho if detection._rho < self._rho_minmax_iter[0] else self._rho_minmax_iter[0]
        self._rho_minmax_iter[1] = detection._rho if detection._rho > self._rho_minmax_iter[1] else self._rho_minmax_iter[1]
        self._theta_minmax_iter[0] = detection._theta if detection._theta < self._theta_minmax_iter[0] else self._theta_minmax_iter[0]
        self._theta_minmax_iter[1] = detection._theta if detection._theta > self._theta_minmax_iter[1] else self._theta_minmax_iter[1]
        self._rvel_minmax_iter[0] = detection._rvel if detection._rvel < self._rvel_minmax_iter[0] else self._rvel_minmax_iter[0]
        self._rvel_minmax_iter[1] = detection._rvel if detection._rvel > self._rvel_minmax_iter[1] else self._rvel_minmax_iter[1]

    def recalculate_minmax(self):
        self._x_minmax = (min([elem._x for elem in self]), max([elem._x for elem in self]))
        self._y_minmax = (min([elem._y for elem in self]), max([elem._y for elem in self]))
        self._theta_minmax = (min([elem._theta for elem in self]), max([elem._theta for elem in self]))
        self._rvel_minmax = (min([elem._rvel for elem in self]), max([elem._rvel for elem in self]))
        self._rho_minmax = (min([elem._rho for elem in self]), max([elem._rho for elem in self]))
        self._mcc_minmax = (min([elem._mcc for elem in self]), max([elem._mcc for elem in self]))

    def modify_iteration(self,selection):
        self._mcc_minmax_iter = selection['mcc_tp'] if selection['mcc_tp'] else self._mcc_minmax
        self._x_minmax_iter = selection['x_tp'] if selection['x_tp'] else self._x_minmax
        self._y_minmax_iter = selection['y_tp'] if selection['y_tp'] else self._y_minmax
        self._rho_minmax_iter = selection['rho_tp'] if selection['rho_tp'] else self._rho_minmax
        self._theta_minmax_iter = selection['theta_tp'] if selection['theta_tp'] else self._theta_minmax
        self._rvel_minmax_iter = selection['rvel_tp'] if selection['rvel_tp'] else self._rvel_minmax

    def test_detection_to_select(self,detection):
        return (self._mcc_minmax_iter[0] <= detection._mcc <= self._mcc_minmax_iter[1] and
                self._x_minmax_iter[0] <= detection._x <= self._x_minmax_iter[1] and
                self._y_minmax[0] <= detection._y <= self._y_minmax[1] and
                self._rho_minmax_iter[0] <= detection._rho <= self._rho_minmax_iter[1] and
                self._theta_minmax_iter[0] <= detection._theta <= self._theta_minmax_iter[1] and
                self._rvel_minmax_iter[0] <= detection._rvel <= self._rvel_minmax_iter[1])

    def get_min_mcc(self):
        return self._mcc_minmax[0]

    def get_max_mcc(self):
        return self._mcc_minmax[1]

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


def cnf_file_read(cnf_file):
        # Read the configuration file
        config = configparser.ConfigParser()
        config.read(cnf_file)  # "./setup.cnf"

        # Get a path to a folder with data
        conf_data = {"datafile": config.get('Datasets', 'data_01')}
        return conf_data

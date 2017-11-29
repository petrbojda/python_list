#!/usr/bin/env python

import data_containers as dc

import numpy as np


def main(config_data):


    # Load Data from .csv file
    if config_data["datafile"]:
        data_path = config_data["datafile"]

        lst_det = dc.DetectionList()
        lst_det.append_data_from_csv(data_path)

        print("filtering: MCCs start at: ", lst_det.get_min_mcc(),
              "and end at: ", lst_det.get_max_mcc())

        print("filtering: No filtering applied yet.")
        print("filtering: MCCs start at: ", lst_det.get_min_mcc(),
                  "and end at: ", lst_det.get_max_mcc())
        print(lst_det.get_array_mcc())
        print(lst_det.get_array_x())
        print(lst_det.get_array_y())

    # Filter the list by the "selection" structure
    selection = {"mcc_tp": None, "x_tp": None, "y_tp": None,
                 "rho_tp": None, "rvel_tp": [0.6, 5], "theta_tp": [40 * np.pi / 180, 58 * np.pi / 180]}
    # Structure 'selection' constrains  data to use as input to the tracker.
    # An exact value or interval of 'mcc', 'azimuth', 'range' ... etc can be
    # specified here to block unwanted data to enter.
    # Programmer point of view: the structure "selection" is used to modify
    # the __next__() method in a DetectionList class.

    if lst_det:
        lst_det.modify_iteration(selection)
        print("filtering: Selection to apply:", selection)
        print("filtering: mcc:", lst_det._mcc_minmax)
        print("filtering: MCCs start at: ", lst_det.get_min_mcc(),
              "and end at: ", lst_det.get_max_mcc())
        print(lst_det.get_array_mcc())
        print(lst_det.get_array_x())
        print(lst_det.get_array_y())


if __name__ == "__main__":
    config_data = dc.cnf_file_read("./setup.cnf")
    if config_data:
        main(config_data)

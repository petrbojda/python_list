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
        print("filtering: The lst_det keys:",lst_det[0].keys())

        print("filtering: No filtering applied yet.")
        print("filtering: MCCs start at: ", lst_det.get_min_mcc(),
                  "and end at: ", lst_det.get_max_mcc())
        print("mcc",lst_det.get_array_mcc())
        print("x",lst_det.get_array_x())
        print("y",lst_det.get_array_y())
        print("rho",lst_det.get_array_rho())
        print("theta",lst_det.get_array_theta_deg())
        print("rvel",lst_det.get_array_rvel())
    else:
        print("filtering: lst_det is empty.")

    # The first filtration: Filter the list by the "selection" structure
    selection = {"mcc_tp": None, "x_tp": None, "y_tp": None,
                 "rho_tp": None, "rvel_tp": [0.6, 5], "theta_tp": [40 * np.pi / 180, 58 * np.pi / 180]}
    # Structure 'selection' constrains  data to use as input to the tracker.
    # An exact value or interval of 'mcc', 'azimuth', 'range' ... etc can be
    # specified here to block unwanted data to enter.
    # Programmer point of view: the structure "selection" is used to modify
    # the __next__() method in a DetectionList class.
    print(90 * "=")
    print("filtering: 2nd, Selection to apply:", selection)
    if lst_det:
        lst_det.modify_iteration(selection)

        print("filtering: mcc:", lst_det._mcc_minmax)
        print("filtering: MCCs start at: ", lst_det.get_min_mcc(),
              "and end at: ", lst_det.get_max_mcc())
        print("mcc", lst_det.get_array_mcc())
        print("x", lst_det.get_array_x())
        print("y", lst_det.get_array_y())
        print("rho", lst_det.get_array_rho())
        print("theta", lst_det.get_array_theta_deg())
        print("rvel", lst_det.get_array_rvel())
    else:
        print("filtering: lst_det is empty.")

    # The second filtration: Filter the list by the "selection" structure
    selection = {"mcc_tp": None, "x_tp": None, "y_tp": None,
                 "rho_tp": None, "rvel_tp": None, "theta_tp": None}
    # Structure 'selection' constrains  data to use as input to the tracker.
    # An exact value or interval of 'mcc', 'azimuth', 'range' ... etc can be
    # specified here to block unwanted data to enter.
    # Programmer point of view: the structure "selection" is used to modify
    # the __next__() method in a DetectionList class.
    print(90 * "=")
    print("filtering: 3th, Selection to apply:", selection)

    if lst_det:
        lst_det.modify_iteration(selection)

        print("filtering: mcc:", lst_det._mcc_minmax)
        print("filtering: MCCs start at: ", lst_det.get_min_mcc(),
              "and end at: ", lst_det.get_max_mcc())
        print("mcc", lst_det.get_array_mcc())
        print("x", lst_det.get_array_x())
        print("y", lst_det.get_array_y())
        print("rho", lst_det.get_array_rho())
        print("theta", lst_det.get_array_theta_deg())
        print("rvel", lst_det.get_array_rvel())
    else:
        print("filtering: lst_det is empty.")


if __name__ == "__main__":
    config_data = dc.cnf_file_read("./setup.cnf")
    if config_data:
        main(config_data)

#!/usr/bin/env python

import data_containers as dc

import numpy as np


def main(config_data):
    selection = {"mcc_tp": None, "x_tp": None, "y_tp": None,
                 "rng_tp": None, "vel_tp": (-5, 5), "az_tp": None}
    # Structure 'selection' constrains  data to use as input to the tracker.
    # An exact value or interval of 'mcc', 'azimuth', 'range' ... etc can be
    # specified here to block unwanted data to enter.


    # Load Data from .csv file
    if config_data["datafile"]:
        data_path = config_data["datafile"]

        lst_det = dc.DetectionList()
        lst_det.append_data_from_csv(data_path)

        print("filtering: MCCs start at: ", lst_det.get_min_mcc(),
              "and end at: ", lst_det.get_max_mcc())


if __name__ == "__main__":
    config_data = dc.cnf_file_read("./setup.cnf")
    if config_data:
        main(config_data)

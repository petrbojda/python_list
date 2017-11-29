#!/usr/bin/env python

import data_containers as dc

import numpy as np


def main(config_data):
    selection = {"beam_tp": config_data["beams_tp"],
                 "mcc_tp": None, "x_tp": None, "y_tp": None,
                 "rng_tp": None, "vel_tp": (-5, 5), "az_tp": None,
                 "trackID_tp": None, }
    # Structure 'selection' constrains  data to use as input to the tracker.
    # An exact value or interval of 'mcc', 'azimuth', 'range' ... etc can be
    # specified here to block unwanted data to enter.


    # Load Data from .mat files
    if config_data["filename"]:
        l = []
        l.append(config_data["path_data_folder"])
        l.append(config_data["filename"])
        leftradar_path = ''.join(l)

        lst_det = dc.DetectionList()
        lst_det.append_data_from_csv(leftradar_path,)

        print("filter_framework: MCC Left starts at: ", mcc_interval_LR[0],
              "and ends at: ", mcc_interval_LR[1])

    # Calculate valid mcc interval for detections to be presented
    if config_data["filename"]:
        mcc_start = mcc_interval_LR[0]
        mcc_end = mcc_interval_LR[1]

    mcc_end = mcc_start + 1000
    print("filter_framework: MCC starts at: ", mcc_start, "MCC ends at: ", mcc_end)
    mcc_step = 1

    #----------------- Filtering loop
    i_prev = mcc_start
    for i in range(mcc_start, mcc_end, mcc_step):  # number of frames

        selection["mcc_tp"] = (i_prev, i)
        #-------------- Left radar filter
        if lst_det_LR:
            lst_det_per_loop_cycle_LR = lst_det_LR.get_lst_detections_selected(selection=selection)

            # TODO: Is it correct to assign this for every iteration? Potential to write
            # more effective code.
            if lst_det_per_loop_cycle_LR:
                print('filter_framework: Number of detections for a LR mcc ', i, 'is: ',
                      len(lst_det_per_loop_cycle_LR))
                track_mgmt_LR.new_detections(lst_det_per_loop_cycle_LR)
                lst_not_assigned_LR,new_track_LR = track_mgmt_LR.port_data("track_init")
                if new_track_LR:
                    print("filter_framework: Type of ported new_track list",type(new_track_LR))
                    print("filter_framework: Type of ported new_track element", type(new_track_LR[-1]))
                else:
                    print("filter_framework: new_track not ported/created")
                rp.static_plotTrackMan_initialization(lst_det_per_loop_cycle_LR,
                                                      lst_not_assigned_LR,
                                                      new_track_LR)
            else:
                print('filter_framework: There is no detection for current LR mcc ',i)

        i_prev = i + 1
        # This line is redundant if only one mcc is being processed per loop cycle.
        # However if mcc_step is different than 1, it might be good to keep it here.


#     TODO: graphical representation of the results

if __name__ == "__main__":
    config_data = dc.parse_CMDLine("./analysis.cnf")
    if config_data:
        main(config_data)

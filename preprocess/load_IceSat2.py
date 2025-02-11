import os.path

import h5py
import numpy as np
from filter.process_IS2_dis_geoid import process_IS2_dis_geoid


def load_IceSat2(filename, beam_name, thr_conf=1):
    # Open the HDF5 file
    with h5py.File(filename, 'r') as f:
        # Read data from the file
        raw_H = f[f'/{beam_name}/heights/h_ph'][:]
        raw_lon = f[f'/{beam_name}/heights/lon_ph'][:]
        raw_lat = f[f'/{beam_name}/heights/lat_ph'][:]
        raw_conf = f[f'/{beam_name}/heights/signal_conf_ph'][
                   :]

        dist_along_track_segment = f[f'/{beam_name}/heights/dist_ph_along'][:]
        geoid = f[f'/{beam_name}/geophys_corr/geoid'][:]
        segment_length = f[f'/{beam_name}/geolocation/segment_length'][:]
        segment_ph_cnt = f[f'/{beam_name}/geolocation/segment_ph_cnt'][:]


    # Ensure the sum of photon counts matches the number of height points
    if np.sum(segment_ph_cnt) != len(raw_H):
        if np.sum(segment_ph_cnt) > len(raw_H):
            surplus_n = np.sum(segment_ph_cnt) - len(raw_H)
            surplus_idx = np.where(np.cumsum(segment_ph_cnt) > len(raw_H))[0]
            if len(surplus_idx) > 1:
                surplus_n -= np.sum(segment_ph_cnt[surplus_idx[1:]])
                segment_ph_cnt[surplus_idx[1:]] = 0
                segment_ph_cnt[surplus_idx[0]] -= surplus_n
            else:
                segment_ph_cnt[surplus_idx] -= surplus_n

    H_corGeoid, dist_ph, flag_seg_num_ph = process_IS2_dis_geoid(segment_ph_cnt, segment_length,
                                                                 dist_along_track_segment, geoid, raw_H)

    # sort by dist_ph
    sorted_indices = np.argsort(dist_ph)
    raw_lon = raw_lon[sorted_indices]
    raw_lat = raw_lat[sorted_indices]
    dist_ph = dist_ph[sorted_indices]
    H_corGeoid = H_corGeoid[sorted_indices]
    raw_conf = raw_conf[sorted_indices]

    # Filter out photons with low confidence
    flag_ocean = raw_conf[:, 1] >= thr_conf

    raw_lon = raw_lon[flag_ocean]
    raw_lat = raw_lat[flag_ocean]
    dist_ph = dist_ph[flag_ocean]
    H_corGeoid = H_corGeoid[flag_ocean]

    return raw_lon, raw_lat, dist_ph, H_corGeoid


if __name__ == '__main__':
    fullfn = "./data/processed_ATL03_20200727124034_04910807_006_01.nc"
    load_IceSat2(fullfn, 'gt1r')

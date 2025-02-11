import numpy as np


def process_IS2_dis_geoid(ph_cnt, seg_length, seg_dist_along_track_ph, seg_geoid, H):
    """
    Process ICESat-2 data by calculating the along-track distance for photons and applying geoid correction.

    Parameters:
    ph_cnt : numpy array
        Photon counts per segment.
    seg_length : numpy array
        Length of each segment.
    seg_dist_along_track_ph : numpy array
        Along-track distance of each photon.
    seg_geoid : numpy array
        Geoid height for each segment.
    H : numpy array
        Height of each photon.

    Returns:
    H_cor_geoid : numpy array
        Heights after geoid correction.
    dis_ph : numpy array
        Along-track distances for each photon.
    flag_seg_group_ph : numpy array
        Group flag for each photon.
    """

    # Initialize arrays
    x = np.zeros_like(seg_length)
    x[1:] = seg_length[:-1]  # Distance of each segment (~20 m)
    seg_length_cumsum = np.cumsum(x)

    compensatory_along_track = np.zeros_like(H)  # Record along-track distances
    compensatory_geoid = np.zeros_like(H)  # Record geoid heights
    flag_seg_group_ph = np.zeros_like(H, dtype=int)  # Flag groups for photons

    idx_ph = 0
    group_num = 1

    cnt_length = len(seg_length_cumsum)

    # Iterate over each segment
    for idx_seg in range(cnt_length):
        temp_cnt_ph = ph_cnt[idx_seg]
        idx_ph_end = temp_cnt_ph + idx_ph

        temp_at = np.full(temp_cnt_ph, seg_length_cumsum[idx_seg])
        temp_geoid = np.full(temp_cnt_ph, seg_geoid[idx_seg])

        compensatory_along_track[idx_ph:idx_ph_end] = temp_at
        compensatory_geoid[idx_ph:idx_ph_end] = temp_geoid

        # Assign group flag to photons
        flag_seg_group_ph[idx_ph:idx_ph_end] = group_num
        group_num += 1
        idx_ph = idx_ph_end

    # Combine distances and apply geoid correction
    dis_ph = seg_dist_along_track_ph + compensatory_along_track
    H_cor_geoid = H - compensatory_geoid  # set the average sea surface = 0 m

    return H_cor_geoid, dis_ph, flag_seg_group_ph

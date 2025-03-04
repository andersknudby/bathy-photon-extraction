import numpy as np

from matplotlib import pyplot as plt

def DBSCAN_circle(dist_ph, H, eps=5, min_samples=5):
    from sklearn.cluster import DBSCAN
    data = np.vstack((dist_ph, H)).T
    # Add index information to the data
    data_with_index = np.hstack((data, np.arange(len(data)).reshape(-1, 1)))

    # DBSCAN
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(data_with_index)
    labels = db.labels_

    # binary labels
    binary_labels = np.where(labels == -1, 0, 1)  # 0 noise, 1 valid
    binary_labels = binary_labels.astype(bool)

    return binary_labels

def DBSCAN_ellipses(dist_ph, H, a=10, b=1, min_samples=5):
    from sklearn.cluster import DBSCAN
    data = np.vstack((dist_ph, H)).T
    # Add index information to the data
    data_with_index = np.hstack((data, np.arange(len(data)).reshape(-1, 1)))

    # define the distance function
    def elliptical_distance(X, Y, a=a, b=b):
        dx = X[0] - Y[0]
        dy = X[1] - Y[1]

        return np.sqrt((dx / a) ** 2 + (dy / b) ** 2)

    # binary labels
    db = DBSCAN(min_samples=min_samples, metric=elliptical_distance).fit(data_with_index)
    labels = db.labels_

    # 二值化标签
    binary_labels = np.where(labels == -1, 0, 1)  # 0 noise, 1 valid
    binary_labels = binary_labels.astype(bool)

    return binary_labels


def DBSCAN_square(x, y, square_w=10, square_h=1, min_points=12):
    """
    Filter noisy datapoint based on density using a square filter box.
    Lai et al., 2022. A Portable Algorithm to Retrieve Bottom Depth of Optically Shallow Waters from Top-of-Atmosphere Measurements. Journal of Remote Sensing 2022. https://doi.org/10.34133/2022/9831947.

    Parameters:
    x : dist of photon
    y : Height of photon
    square_w : int, optional
    square_h : int, optional
    min_points : int, optional

    Returns:
    binary_labels -> np.bool

    """

    idx_row = np.arange(len(x))

    num_points = len(x)
    record = np.full(num_points, np.nan)

    for idx in range(num_points):
        point_x = x[idx]
        point_y = y[idx]
        d_y = np.abs(y - point_y)
        d_x = np.abs(x - point_x)
        # if np.abs(point_y) < 2:
        #     square_h /= 2
        flag = (d_x < square_w) & (d_y < square_h)
        record[idx] = max(0, np.sum(flag) >= min_points)  # 0 noise, 1 valid

    # Filter points based on record
    binary_labels = record.astype(bool)

    return binary_labels




if __name__ == '__main__':
    # data = np.load('test_DBSCAN.npz')
    # dist = data['arr_0']
    # H = data['arr_1']

    pass
from matplotlib import pyplot as plt

from method.DBSCAN import DBSCAN_circle, DBSCAN_ellipses, DBSCAN_square
from preprocess.load_IceSat2 import load_IceSat2


def draw_fig(ax, dist, H, label=None, title=''):
    "label = 1 is valid point"
    ax.set_xlabel('Along track distance (m)')
    ax.set_ylabel('Photon Height (m)')
    ax.plot(dist, H, 'o', color='grey', markersize=.5, label='raw data')
    if label is not None:
        ax.plot(dist[label], H[label], 'ro', markersize=.5, label='valid data')
    else:
        ax.plot(dist, H, 'ro', markersize=.5, label='all data')
    ax.set_title(title, loc='left')
    ax.legend()


if __name__ == '__main__':
    fullfn = "./data/processed_ATL03_20200727124034_04910807_006_01.nc"

    _, _, dist, H = load_IceSat2(fullfn, 'gt1r')

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    draw_fig(ax, dist, H, title='all points')
    plt.tight_layout()
    plt.savefig('raw_rs.png', dpi=300)
    plt.show()

    # undersurface points
    flag_undersurface = H < 0
    dist = dist[flag_undersurface]
    H = H[flag_undersurface]

    # DBSCAN
    eps = 4
    min_points = 3

    label = DBSCAN_circle(dist, H, eps=eps, min_samples=min_points)

    # DBSCAN_ellipses_pro
    a, b, = 5, 1  # ellipse parameters
    min_points = 2  # min points in a cluster
    label_dbscan = DBSCAN_ellipses(dist, H, a=a, b=b, min_samples=min_points)

    # DBSCAN_square
    square_w, square_h = 10, 1  # square parameters
    min_points_square = 4  # min points in a cluster
    label_DBSCAN_square = DBSCAN_square(dist, H, square_w=square_w, square_h=square_h, min_points=min_points_square)

    # plot
    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    draw_fig(axes[0], dist, H, label, title='DBSCAN circle filter')
    draw_fig(axes[1], dist, H, label_dbscan, title='DBSCAN ellipses filter')
    draw_fig(axes[2], dist, H, label_DBSCAN_square, title='DBSCAN square filter')

    plt.tight_layout()
    plt.savefig('test_rs.png', dpi=300)
    plt.show()

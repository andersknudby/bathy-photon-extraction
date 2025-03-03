# bathy-photon-extraction
Repository for ICESat-2 bathymetric photon extraction algorithms.

The ATLAS sensor on ICESat-2 is a space-based photon-counting lidar instrument. One of the most fundamental ATLAS products available to the public is ATL03, which contains geolocated photons (along with a host of other useful information). The extract information on water depth from ATL03, it is necessary to (1) identify the photon locations that represent the water surface, (2) identify the photon locations that represent the water bottom, and (3) calculate the vertical distance between them, corrected for refraction effects.

(1) and (3) above are relatively easy - (2) is not. Much research has been oriented toward (2), and many algorithms have been published in the academic literature along with demonstrations of their effectiveness for a few data sets. However, most of these publications have not shared the implementation of those algorithms in code, making comparisons between algorithms, for different environmental contexts, difficult. As a result, it is difficult to judge if real progress is being made toward better algorithms, more accurate identification of seafloor photons, and thus better use of ICESat-2 data for water depth mapping.

With this repository we aim to facilitate such comparisons in an effort to better assess the capability of individual algorithms, find their strengths and weaknesses in different environmental contexts, and push the global research community forward toward improved use of ICESat-2 data for water depth mapping.



# Python environment

## Installation Steps

1. Create a new Python environment

```bash
# Using conda (recommended)
conda create -n bathy-photon python=3.12 pip
conda activate bathy-photon
```

2. Install dependencies
```bash
pip install numpy matplotlib h5py scikit-learn icepyx
```


3. Clone the repository

```bash
git clone https://github.com/andersknudby/bathy-photon-extraction.git
cd bathy-photon-extraction
```


## File Structure

- `main_comparison.py`: Main program for comparing different DBSCAN algorithms
- `method/DBSCAN.py`: Contains three DBSCAN algorithm implementations (circular, elliptical, and square)
- `preprocess/load_IceSat2.py`: Data loading and preprocessing functions
- `preprocess/process_IS2_dis_geoid.py`: Processes geographic location and elevation information of ICESat-2 data
- `data/`: Contains sample data files

# Usage Instructions

## Running the Comparison Program

Run the `main_comparison.py` script to compare different clustering methods for extracting bathymetric photon data:

```bash
python main_comparison.py
```

This script will:

1. Load preprocessed ICESat-2 ATL03 data
2. Plot and save raw photon data (raw_rs.png)
3. Apply three different DBSCAN clustering methods to filter data
4. Plot and save a comparison of the three methods

## Customizing Parameters

You can modify the following parameters in `main_comparison.py` to adjust the algorithms:

1. **Circular DBSCAN**:
   - `eps`: Neighborhood radius
   - `min_points`: Minimum sample count

2. **Elliptical DBSCAN**:
   - `a`, `b`: Ellipse major and minor axis parameters
   - `min_points`: Minimum sample count

3. **Square DBSCAN**:
   - `square_w`, `square_h`: Square width and height parameters
   - `min_points_square`: Minimum sample count
   - References Lai et al., 2022. A Portable Algorithm to Retrieve Bottom Depth of Optically Shallow Waters from Top-of-Atmosphere Measurements. Journal of Remote Sensing 2022. https://doi.org/10.34133/2022/9831947 




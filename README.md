# bathy-photon-extraction
Repository for ICESat-2 bathymetric photon extraction algorithms.

The ATLAS sensor on ICESat-2 is a space-based photon-counting lidar instrument. One of the most fundamental ATLAS products available to the public is ATL03, which contains geolocated photons (along with a host of other useful information). The extract information on water depth from ATL03, it is necessary to (1) identify the photon locations that represent the water surface, (2) identify the photon locations that represent the water bottom, and (3) calculate the vertical distance between them, corrected for refraction effects.

(1) and (3) above are relatively easy - (2) is not. Much research has been oriented toward (2), and many algorithms have been published in the academic literature along with demonstrations of their effectiveness for a few data sets. However, most of these publications have not shared the implementation of those algorithms in code, making comparisons between algorithms, for different environmental contexts, difficult. As a result, it is difficult to judge if real progress is being made toward better algorithms, more accurate identification of seafloor photons, and thus better use of ICESat-2 data for water depth mapping.

With this repository we aim to facilitate such comparisons in an effort to better assess the capability of individual algorithms, find their strengths and weaknesses in different environmental contexts, and push the global research community forward toward improved use of ICESat-2 data for water depth mapping.

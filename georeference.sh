#!/bin/sh

# apply static georef points from QGIS
gdal_translate -q -of GTiff -gcp 33.5074 267.3 -79.7614 42.0032 -gcp 8.00829 368.289 -80.5192 39.7217 -gcp 7.50461 267.048 -80.5197 41.9771 -gcp 204.949 296.262 -74.6933 41.3638 -gcp 203.163 349.649 -74.7197 40.1541 -gcp 438.516 25.0506 -67.7898 47.068 -gcp 390.281 6.4947 -69.2297 47.4577 -gcp 453.382 119.909 -67.3393 45.1275 -gcp 197.237 401.003 -74.9776 38.9313 -gcp 300.36 307.86 -71.8492 41.077 -gcp 357.743 262.951 -70.2301 42.0806 -gcp 245.472 264.614 -73.491 42.0451 -gcp 252.125 232.18 -73.263 42.7458 -gcp 149.002 169.808 -76.3756 44.105 -gcp 319.904 113.048 -71.2834 45.2997 "$1" georef_temp.tif
gdalwarp -q -r lanczos -tps -co COMPRESS=NONE  georef_temp.tif georef_temp2.tif

# warp to web mercator
gdalwarp -q -s_srs EPSG:4326 -t_srs EPSG:3857 -r bilinear georef_temp2.tif georef_temp3.tif

# move files around, cleanup
mv georef_temp2.tif "$1"
rm -f georef_temp.tif georef_temp3.gif

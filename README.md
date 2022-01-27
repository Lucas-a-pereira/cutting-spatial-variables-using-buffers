# cutting-spatial-variables-using-buffers
### This work is divided into two scripts:
- In the first script, the tree cover and tree loss tiles downloaded from [Global Forest Change](https://storage.googleapis.com/earthenginepartners-hansen/GFC-2020-v1.8/download.html) are being imported into GRASS GIS. They are then combined to form two global mosaics, one of forest cover and one of forest loss.

- In the second script, a five kilometer buffer is made around several points that represent the exact location of primate communities. These buffers are used to cut the forest cover mosaic made in the first script, and then the forest loss mosaic is used to discount the "deforested" pixels using the sampling year of primate communities as the base year. This processing of spatial data using sampling years and discounting gross forest loss allowed us to have a more accurate representation of forest cover for each sampled area.

This processing was made for the neotropical and central africa regions. And this is what we have at the end:

![alt text](https://github.com/Lucas-a-pereira/cutting-spatial-variables-using-buffers/blob/main/com_011_treecover_GFW_2000_deforestation_cgs_wgs84.jpg?raw=true)

After this processing, binary maps were made where pixels with value 0 represent forest loss and pixels with value 1 indicate forest presence. The final product looked like this:

![alt text](https://github.com/Lucas-a-pereira/cutting-spatial-variables-using-buffers/blob/main/com_011_treecover_GFW_2000_deforestation_threshold70_binary_cgs_wgs84.jpg?raw=true)

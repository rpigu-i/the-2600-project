[code]
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    File name: 3DMaker.py

#    Produce a 3D SBS image from two stills
#    WARNING: This script is written for Windoze
#             and needs adaptation for Linux, see below.

from gimpfu import *
import os

# Function to crop to 16:9 if necessary, centered
def cropper( image ):
#    Record original dimensions
    w_orig = image.width
    h_orig = image.height
   
#    Target ratio
    ratio = 16.0 / 9.0

#    Compare picture to target ratio
#    If image is too high or too wide, need to crop (centered)
#    If ratio is ok, keep all pixels
    if (w_orig / h_orig) < (ratio - 0.00001):
        w_new = w_orig
        h_new = int(w_orig / ratio)
        offx = 0
        offy = int((h_orig - h_new) / 2)
    elif (w_orig / h_orig) > (ratio + 0.00001):
        w_new = int(h_orig * ratio)
        h_new = h_orig
        offx = int((w_orig - w_new) / 2)
        offy = 0
    else:
        w_new = w_orig
        h_new = h_orig
        offx = 0
        offy = 0
   
    pdb.gimp_image_crop( image, w_new, h_new, offx, offy )
   
    return

# Function to rescale to half-width of 1920 x 1080, distorting image
def resizer( image ):
    pdb.gimp_image_scale( image, 960, 1080 )
   
    return
   
# The registered script called by main()
# Sorry it's not more Pythonic
def threedmaker( full_filename_left, full_filename_right ) :

#    Left image load
    image_left = pdb.gimp_file_load( full_filename_left, full_filename_left )
    display_left = gimp.Display( image_left )

#    Record path information, compute new file's filename
    folder_left = os.path.dirname( os.path.abspath( full_filename_left ) )
    filename_left_new = "3D SBS_" + pdb.gimp_image_get_name( image_left )

#    Right image load
    image_right = pdb.gimp_file_load( full_filename_right, full_filename_right )
    display_right = gimp.Display( image_right )

#    Prepend "3D SBS_" to left image filename, this is how the final file will be saved
    pdb.gimp_image_set_filename( image_left, filename_left_new )

#    Crop the images if necessary
    cropper( image_left )
    cropper( image_right )

#    Resize (reduce dimensions) each image to 1080p
    resizer( image_left )
    resizer( image_right )

#    We will work from the left image; we will copy to right image in the left image's container
#    Copy right image to memory and paste in left image's container
    pdb.gimp_edit_copy( pdb.gimp_image_get_active_drawable( image_right ) )

#    Increase canvas size and paste in data from right image
    pdb.gimp_image_resize( image_left, 1920, 1080, 0, 0 )
    layer_work = pdb.gimp_image_get_active_layer( image_left )
    floating_sel = pdb.gimp_edit_paste( pdb.gimp_image_get_active_drawable( image_left ), TRUE )

#    Move right image pixels to appropriate position
    pdb.gimp_layer_resize( layer_work, 1920, 1080, 0, 0 )
    pdb.gimp_layer_translate( floating_sel, 960, 0 )

#    Merge layers
    pdb.gimp_image_flatten( image_left )

#    Save new picture in left image's original folder
#    WARNING: For Linux, the directory separator is written with a single forward slash '/'
    pdb.gimp_file_save( image_left, pdb.gimp_image_get_active_drawable( image_left ), folder_left + "\\" + filename_left_new,  folder_left + "\\" + filename_left_new )

#    End of script, free memory
    pdb.gimp_display_delete( display_right )
    pdb.gimp_image_delete( image_right )
    pdb.gimp_display_delete( display_left )
    pdb.gimp_image_delete( image_left )

    return

# This is the plugin registration function
register(
    "threedmaker_script",
    "Merges two images into one fitting 3D SBS standard",
    "Merges two images (left eye and right eye views) in one 3D side-by-side image",
    "TFE Guy a.k.a. The Man",
    "TFE Guy a.k.a. The Man à la maison",
    "Août 2014",
    "<Toolbox>/MyScripts/3D Maker...",
    "",
    [
#    WARNING: For Linux, the directory separator is written with a single forward slash '/'
      (PF_FILENAME, 'string_left', 'Path\\image for left eye', 'C:\\Photos\\left.JPG'),
      (PF_FILENAME, 'string_right', 'Path\\image for right eye', 'C:\\Photos\\right.JPG')
    ],
    [],
    threedmaker,
    )

main()
[/code]

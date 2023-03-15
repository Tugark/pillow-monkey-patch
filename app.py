import os

from PIL import Image
from PIL import TiffImagePlugin

# load monkey patch
from monkey_patch import ImageFileDirectory_v2

TEST_FILE = f'{os.path.dirname(__file__)}/jester.jpg'

# Exif-Tags
GPS_TAG = 0x8825
IMAGE_DIRECTION = 0x0011
MODEL = 0x0110
FOCALLENGTH = 0x920A
EXIFIMAGEWIDTH = 0xA002
FOCALPLANEXRESOLUTION = 0xA20E
EXIFIMAGEHEIGHT = 0xA003
FOCALPLANEYRESOLUTION = 0xA20F
MODIFYDATE = 0x0132


def _update_exif_dict(exif_dict, values_to_change):
    for value in values_to_change:
        exif_dict.update({value[0]: value[1]})
    return exif_dict


if __name__ == '__main__':
    # monkey patch the library
    TiffImagePlugin.ImageFileDirectory_v2 = ImageFileDirectory_v2

    # same code as in toolbox
    image = Image.open(TEST_FILE)
    exif = image.getexif()

    gps_exif = exif[GPS_TAG]
    gps_values_to_change = [
        (IMAGE_DIRECTION, 314)
    ]
    updated_gps = _update_exif_dict(gps_exif, gps_values_to_change)
    exif[GPS_TAG] = gps_exif
    print(updated_gps)

    image.save(f'{TEST_FILE}__test.jpg', "JPEG", exif=exif)

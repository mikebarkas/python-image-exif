import argparse
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def get_exif(image_file):
    """Extracts data from image file"""
    try:
        file = Image.open(image_file)
        return file._getexif()
    except:
        return None


def decode_tags(data):
    """Decodes key tags to human readable keys"""
    return_dict = {}
    for (tag, value) in data.items():
        decoded = TAGS.get(tag, tag)
        return_dict[decoded] = value
    return return_dict


def camera_tags():
    """Just list the fields needed for the camera information"""
    return {'DateTimeOriginal', 'Make', 'Model'}


def camera_data(data):
    decoded = decode_tags(data)
    return {key:value for key,value in decoded.items() if key in camera_tags()}


def get_lat_lon(exif_data):
    try:
        gps_lat = exif_data[34853][2]
        lat = convert_to_degrees(gps_lat)
        gps_lon = exif_data[34853][4]
        lon = convert_to_degrees(gps_lon)

        if exif_data[34853][1] != 'N':
            lat *= -1

        if exif_data[34853][3] != 'E':
            lon *= -1

        return lat, lon

    except KeyError:
        return None


def convert_to_degrees(value):
    """Change gps exif data into degrees."""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='Image file name')
    args = parser.parse_args()

    if args.image:
        exif = get_exif(args.image)
        # Print camera information.
        camera_info = camera_data(exif)
        print(camera_info)
        # Pring gps information.
        gps = get_lat_lon(exif)
        print(gps)
    else:
        print(parser.usage)


if __name__ == '__main__':
    main()


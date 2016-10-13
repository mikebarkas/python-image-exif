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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='Image file name')
    args = parser.parse_args()

    if args.image:
        exif = get_exif(args.image)
        camera_info = camera_data(exif)
        print(camera_info)
    else:
        print(parser.usage)


if __name__ == '__main__':
    main()


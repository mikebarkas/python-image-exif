import argparse
from PIL import Image
from PIL.ExifTags import TAGS


def get_metadata(image_name):
    try:
        img_file = Image.open(image_name)
        data = img_file._getexif()
        if data:
            for (tag, value) in data.items():
                tagname = TAGS.get(tag, tag)
                print(str(tagname) + '\t' + str(value) + '\n')
    except:
        print('Image data not found')



def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('img', help='Image file name')
    args = parser.parse_args()

    if args.img:
        get_metadata(args.img)
    else:
        print(parser.usage)


if __name__ == '__main__':
    Main()


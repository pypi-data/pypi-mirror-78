from PIL import Image
import argparse
from resizeimage import resizeimage

__version__ = "0.1.0"

def get_parser():
    parser = argparse.ArgumentParser(description='Resize an image')

    parser.add_argument('--image', type=str, required=True, help='Path to source image')
    parser.add_argument('--width', type=int, required =True, help='Width to resize. Will take min(ImageWidth, width).')
    parser.add_argument('--height', type=int, required=True, help='Height to resize. Will take min(ImageHeight, height')
    parser.add_argument('--destination', type=str, required=True, help='Path to save resized image')
    
    return parser.parse_args()


def resize_image(filename, width, height, destination):
    with open(filename, 'r+b') as f:
        with Image.open(f) as image:
            imageWidth, imageHeight = image.size
            resizedWidth = min(imageWidth, width)
            resizedHeight = min(imageHeight, height)
            
            cover = resizeimage.resize_cover(image, [resizedWidth, resizedHeight])
            cover.save(destination, image.format)
    return

def main():
    args = get_parser()
    resize_image(args.image, args.width, args.height, args.destination)

main()

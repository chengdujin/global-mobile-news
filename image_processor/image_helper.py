#!/usr/bin/env python 
#-*- coding: utf-8 -*- 

# image_scraper is used to find all images from
# a web page
#
# @author Jin Yuan
# @contact jinyuan@baidu.com
# @created Jul. 23, 2013

import sys 
reload(sys) 
sys.setdefaultencoding('UTF-8')
sys.path.append('..')

from administration.config import IMAGES_LOCAL_DIR
from administration.config import IMAGES_PUBLIC_DIR
from administration.config import MIN_IMAGE_SIZE
from administration.config import THUMBNAIL_SIZE
from administration.config import TRANSCODED_LOCAL_DIR
from BeautifulSoup import BeautifulSoup
import Image

def find_images(content=None):
    """
    find out all images from content and its size info
    """
    if not content:
        return None

    # determine the type of content
    if content.startswith(TRANSCODED_LOCAL_DIR):
        # then its a file
        f = open(content, 'r')
        content = f.read()
    
    soup = BeautifulSoup(content.decode('utf-8'))
    images_new = []
    if soup.img:
        if soup.img.get('src'):
            return normalize(soup.img['src'])
    return None
             

def find_biggest_image(images=None):
    """
    find the biggest in resolution from a pile of images
    """
    if not images:
        return None
    
    biggest = None
    for image in images:
        resolution_max = MIN_IMAGE_SIZE[0] * MIN_IMAGE_SIZE[1] 
        resolution_image = int(image['width']) * int(image['height'])
        if resolution_image > resolution_max:
            biggest = image
            resolution_max = resolution_image
    return biggest 


# TODO: boundary checker
def scale_image(image=None, size_expected=MIN_IMAGE_SIZE, resize_by_width=True, crop_by_center=True, relative_path=None):
    """
    resize an image as requested
    crop_by: center, width, height
    """
    if not image or not size_expected or not relative_path:
        return None

    width = int(image['width'])
    height = int(image['height'])
    image_url = image['url']
    width_expected = size_expected[0]
    height_expected = size_expected[1]

    if width > width_expected and height > height_expected:
        if resize_by_width:
            height_new = int(width_expected / width * height)
            width_new = width_expected
        else:
            width_new = int(height_expected / height * width)
            height_new = height_expected

        # larger and equal than is important here
        if width_new >= width_expected and height_new >= height_expected:
            try:
                # resize
                image_pil = Image.open(image_url)
                size_new = width_new, height_new
                image_pil.thumbnail(size_new, Image.ANTIALIAS)
                # crop
                if crop_by_center:
                    left = (width_new - width_expected) / 2
                    top = (height_new - height_expected) / 2
                    right = (width_new + width_expected) / 2
                    bottom = (height_new + height_expected) / 2
                    image_pil.crop(left, top, right, bottom)
                else:
                    left = 0
                    top = 0
                    right = width_expected
                    bottom = height_expected
                    image_pil.crop(left, top, right, bottom)
                # storing
                image_pil = image_pil.convert('RGB')
                image_pil.save(xxxxxxxxxxxx, 'JPEG')
                return image_web_path, image_local_path
            except IOError as k:
                raise Exception('ERROR: %s is not an image' % image_url)
        else:
            return scale_image((image, size_expected, not resize_by_width, not crop_by_center, relative_path)
    else:
        return None
        

def normalize(images):
    """
    for list of images, remove images that don't match with MIN_IMAGE_SIZE;
    for an image, return None if it doesn't matches with MIN_IMAGE_SIZE
    """
    def _check_image(image):
        """
        check an image if it matches with MIN_IMAGE_SIZE
        """
        if not image:
            raise Exception('ERROR: Method not well formed!')

        try:
            if thumbnail.is_valid_image(image):
                width, height = thumbnail.get_image_size(image)
                return {'url':image, 'width':width, 'height':height}
            else:
                return None
        except IOError as k:
            return None

    if isinstance(images, str):
        image = _check_image(images)
        return [image] if image else None
    elif isinstance(images, list):
        images_new = []
        for image in images:
            image_new = _check_image(image)
            if image_new:
                images_new.append(image_new)
        return images_new if images_new else None

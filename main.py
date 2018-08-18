import os
import sys
import urllib.parse
import urllib.request
from zipfile import ZipFile

import cssutils
import requests
from bs4 import BeautifulSoup
from wand.image import Image

# The Line store URL format.
LINE_URL = "https://store.line.me/stickershop/product/"


def dl_stickers(page):
    images = page.find_all('span', attrs={"style": not ""})
    for i in images:
        image_url = i['style']
        image_url = cssutils.parseStyle(image_url)
        image_url = image_url['background-image']
        image_url = image_url.replace('url(', '').replace(')', '')
        image_url = image_url[1:-15]
        response = urllib.request.urlopen(image_url)
        resize_sticker(response, image_url)


def resize_sticker(image, filename):
    with Image(file=image) as img:
        if img.width > img.height:
            ratio = 512.0 / img.width
            img.resize(512, int(round(img.height * ratio)), 'mitchell')
        elif img.width == img.height:
            img.resize(512, 512)
        else:
            ratio = 512.0 / img.height
            img.resize(int(round(img.width * ratio)), 512, 'mitchell')

        img.save(filename=("downloads/" + filename.split(sep='/')[6] + ".png"))


def save_stickers(page, title):
    dl_stickers(page)

    with ZipFile(title + '.zip', 'w') as sticker_zip:
        for root, dirs, files in os.walk("downloads/"):
            for file in files:
                sticker_zip.write(os.path.join(root, file))
                os.remove(os.path.join(root, file))


if len(sys.argv) > 1:
    sticker_url = sys.argv[1]

    request = requests.get(sticker_url).text
    sticker_page = BeautifulSoup(request, "html.parser")
    sticker_title = sticker_page.title.string

    save_stickers(sticker_page, sticker_title)
else:
    print("Usage: " + sys.argv[0] + " (URL_OF_STICKER_PACK)")
    sys.exit()

#!/usr/bin/env

from lxml import html
import requests
import shutil
import rfc6266

root_url = "http://www.justinmaller.com"
gallery_url = root_url + "/wallpapers/"
image_link_descriptor = '//a[@class="image"]/@href'
wallpaper_directory = '/Users/tgraboski/Pictures/wallpapers/JustinMaller'

page = requests.get(gallery_url)
tree = html.fromstring(page.content)

image_page_links = tree.xpath(image_link_descriptor)
img_urls = []

for image_page_link in image_page_links:
    image_page = requests.get(root_url + image_page_link)
    image_tree = html.fromstring(image_page.content)
    img_urls.append(image_tree.xpath('//div[@id="wallwindow"]/img/@src')[0])

print "URLs fetched: " + str(len(img_urls))

for img_url in img_urls:
    response = requests.get(img_url, stream=True)
    path = wallpaper_directory + "/" + rfc6266.parse_requests_response(response).filename_unsafe
    if (response.status_code == 200):
        with open(path, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

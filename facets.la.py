#!/usr/bin/env

from lxml import html
import requests
import shutil
import rfc6266


def get_tree_from_url(url):
    page = requests.get(url)
    return html.fromstring(page.content)


def save_image_from_url(url, directory):
    response = requests.get(url, stream=True)
    path = directory + "/" + rfc6266.parse_requests_response(response).filename_unsafe

    if (response.status_code == 200):
        print 'Saving to {}'.format(path)
        with open(path, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)


def get_image_url(gallery_url):
    bits = gallery_url.split('/')
    return 'http://www.facets.la/wallpaper/W_{}_{:0>3d}.jpg'.format(bits[3], int(bits[4]))


def crawl_and_collect(url, crawl_xpath, collect_xpath, depth=0):
    tree = get_tree_from_url(url)
    collected_values = []

    if (depth > 0):
        links_to_crawl = tree.xpath(crawl_xpath)
        for link_to_crawl in links_to_crawl:
            collected_values.extend(crawl_and_collect(link_to_crawl, crawl_xpath, collect_xpath, depth - 1))

    collected_values.extend(tree.xpath(collect_xpath))
    return collected_values


root_url = "http://www.facets.la"
gallery_url = root_url
wallpaper_directory = '/Users/tgraboski/Pictures/wallpapers/JustinMaller'
img_gallery_urls = crawl_and_collect(root_url, '//div[@id="search-box-next"]//a/@href', '//div[@class="thumb-image"]/a/@href', 10)
img_urls = [get_image_url(x) for x in img_gallery_urls]
for img_url in img_urls:
    save_image_from_url(img_url, wallpaper_directory)

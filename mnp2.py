import os
import random

import requests
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

g_start = 0
g_end = 1000
url0 = "https://www.xsnvshen.com/girl/"
url1 = "https://www.xsnvshen.com/album/"
url2 = "https://img.xsnvshen.com/album/"


def get_album(url):
    ua = UserAgent()
    t_referer = url
    my_headers = {'User-Agent': ua.random, 'referer':t_referer}
    response = requests.get(url, headers=my_headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    div_class_star_mod = soup.find("div", attrs={"class": "star-mod-bd"})
    if div_class_star_mod:
        a_tags = div_class_star_mod.find_all("a")
        albums = []
        for a_tag in a_tags:
            href = a_tag.get("href")
            album = href.split("/")[-1]
            albums.append(album)
    else:
        print("未找到指定的div标签")

    return albums


def generate_image_urls(base_url, start, end):
    image_urls = []
    for i in range(start, end + 1):
        image_url = base_url.replace("000.jpg", f"{i:03}.jpg")
        image_urls.append(image_url)
    return image_urls


def download_image(url, save_path, album_num):
    ua = UserAgent()
    r_referer = url1 + album_num
    my_headers = {'User-Agent': ua.random, 'referer': r_referer}

    time.sleep(0.2)
    response = requests.get(url, headers=my_headers, timeout=10, )
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {url}")


def doit(girl_num, album_num):
    fail_count = 0
    base_url = url2 + girl_num + "/" + album_num + "/" + "000.jpg"
    img_urls = generate_image_urls(base_url, g_start, g_end - 1)
    os_path = "D:" + "\\" + "WC" + "\\" + "output" + "\\" + girl_num + "\\" + album_num

    if not os.path.exists(os_path):
        os.makedirs(os_path)

    for i, img_url in enumerate(img_urls):
        print(f"Downloading image {i + 1}/{len(img_urls)}: {img_url}")
        pic_name = img_url[-7:]
        save_path = f"{os_path}/{pic_name}"
        try:
            download_image(img_url, save_path, album_num)
        except Exception as e:
            print(f"Failed to download image: {e}")
            fail_count = fail_count + 1
            if fail_count > random.randint(2,4):
                break


def main():
    girl_num = input("请输入艺人5位编号: ")
    album_num = input("请输入专辑5位编号，所有专辑输入0: ")
    girl_url = url0 + girl_num

    if album_num != '0':
        doit(girl_num, album_num)
    else:
        albums = get_album(girl_url)
        for album_num in albums:
            doit(girl_num, album_num)


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup as soup
import re
import urllib3
import urllib
import time

# url = 'https://film-grab.com/category/1-371/' #4
# url = 'https://film-grab.com/category/2-001/' #1
# url = 'https://film-grab.com/category/2-201/' #1
# url = 'https://film-grab.com/category/1-751/' #1
# url = 'https://film-grab.com/category/2-351/' # 12
#url = 'https://film-grab.com/category/1-661/' #3
#url = 'https://film-grab.com/category/1-781/' #1
url = 'https://film-grab.com/category/1-851/' #12

def source_img(url):
    links = []
    for x in range(1, 13, 1):
        txt = url+'page/'+str(x)+'/'
        links.append(txt)
    links[0] = url
    # links.append(url)  # for singe processing use this line and comment out the for loop

    for l in links:
        page = requests.get(l)
        html = soup(page.text, 'html.parser')
        result = html.find_all(attrs={'class':'popup-image'})
        result[0].find_all('img')[0].get('data-large-file')

        img_links = []
        title = []
        for each in result:
            img_links.append(each.find_all('img')[0].get('data-large-file'))
            title.append(each.find_all('img')[0].get('data-image-title'))

        for url in img_links:
            filename = url.split('/')[-1]
            r = requests.get(url, allow_redirects=True)
            time.sleep(3)
            open('images/movie_pics/'+filename, 'wb').write(r.content)

source_img(url)

# -*- coding: utf-8 -*-

import time
import urlparse
import requests
import lxml.html
import re

re_num = re.compile(r'\(\d+\)')
def get_celebrities(html_doc):
    celebs = html_doc.xpath('//div[@class="celeb"]')
    for celeb in celebs:
        link = celeb.xpath('descendant::a[2]')[0]
        name = link.text.strip()
        name = re_num.sub('', name).strip().encode('utf-8')

        print 'retrieving: {name}...'.format(name=name)

        url = 'http://www.imdb.com/search/name?name={name}'.format(name=name.replace(' ', '+'))
        celeb_search_html = requests.get(url).content
        celeb_search_doc = lxml.html.fromstring(celeb_search_html)
        target_elem = celeb_search_doc.xpath('//table[@class="results"]/*/td[@class="name"]/a')
        if not target_elem: continue
        target_elem = target_elem[0]
        celeb_url = urlparse.urljoin('http://www.imdb.com' ,target_elem.attrib['href'])

        celeb_doc = lxml.html.fromstring(requests.get(celeb_url).content)
        image_elem = celeb_doc.xpath('//td[@id="img_primary"]/a/img')
        if not image_elem: continue
        image_elem = image_elem[0]
        celeb_image_url = image_elem.attrib['src']

        r = requests.get(celeb_image_url)
        if r.status_code == 200:
            with open('orig/{name}.jpg'.format(name=name), 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
        time.sleep(1)
        

def get_celebrity_list():
    for alphabet in list('ABCDEFGIHJKLMNOPQRSTUVWXYZ'):
        current_page = 1
        while True:
            list_url = 'http://www.posh24.com/celebrities/{c}/{page}'.format(c=alphabet,
                                                                             page=current_page)
            print list_url
            list_html = requests.get(list_url).content
            doc = lxml.html.fromstring(list_html)

            celebrities = get_celebrities(doc)


            list_links = doc.xpath('//div[@class="navigationMenu"]/*/span[@class="links"]/a')
            next_page = False
            for link in list_links:
                page = int(link.attrib['href'].split('/')[-1])
                if page <= current_page:
                    continue

                current_page = page
                break
            else:
                break # no next page

if __name__ == '__main__':
    get_celebrity_list()

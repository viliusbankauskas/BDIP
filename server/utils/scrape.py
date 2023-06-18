import requests
import regex as re
from bs4 import BeautifulSoup
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

def description_scrape(title):
    urlpage =  'https://en.wikipedia.org/wiki/' + title
    page = requests.get(urlpage).text
    soup = BeautifulSoup(page,'lxml')

    text = ''
    for paragraph in soup.find_all('p'):
        if len(text) >= 400:
            break
        text += paragraph.text
        
    limited_text = text[:400]
    return limited_text

def download_image(link, id):
    local_image_path = '{}.jpg'.format(id)
    urllib.request.urlretrieve('https:'+ link, local_image_path)
    return local_image_path

def get_title_imglink(qwiki_id):
    urlpage =  'https://www.wikidata.org/wiki/' + qwiki_id
    page = requests.get(urlpage).text
    soup = BeautifulSoup(page, 'html.parser')
    title_element = soup.find(class_='wikibase-title-label')
    title = title_element.text
    a_tag = soup.find('a', {'data-lat': True, 'data-lon': True})

    if a_tag:
        lat = a_tag['data-lat']
        lon = a_tag['data-lon']
    else:
        print("Latitude and longitude not found")
        lat = 0
        lon = 0
        
    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
        if re.search('wikipedia/.*/thumb/', link) and not re.search('.svg', link):
            local_image_path = download_image(link, qwiki_id)
            description = description_scrape(title)
            return title, lat, lon, description, local_image_path

    return title, lat, lon, None, None

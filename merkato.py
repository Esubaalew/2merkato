from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import logging

DOMAIN = 'https://www.2merkato.com'

def get_categories(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')

        categories = soup.find_all('div', {'class': 'row-fluid mtree_category'})
        category_list = []

        for category in categories:
            a_element = category.find('a')
            span_element = category.find('span', {'class': 'count'})

            category_dict = {
                'name': a_element.get_text(strip=True),
                'href': DOMAIN + a_element['href'],
                'count': span_element.get_text(strip=True)[1:-1],
                'subcategories': get_subcategories(DOMAIN + a_element['href']) 
            }

            category_list.append(category_dict)

        return category_list

    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return []

def get_subcategories(subcategory_url):
    try:
        req = Request(subcategory_url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')

        subcategories_div = soup.find('div', {'class': 'row-fluid mtree_sub_category'})
        subcategory_list = []

        if subcategories_div:
            ul_element = subcategories_div.find('ul', {'class': 'pad10'})
            if ul_element:
                for li_element in ul_element.find_all('li'):
                    a_element = li_element.find('a')
                    span_element = li_element.find('span', {'class': 'count'})

                    subcategory_dict = {
                        'name': a_element.get_text(strip=True),
                        'href': DOMAIN + a_element['href'],
                        'count': span_element.get_text(strip=True)[1:-1]
                    }

                    subcategory_list.append(subcategory_dict)

        return subcategory_list

    except Exception as e:
        logging.error(f"Error scraping {subcategory_url}: {e}")
        return []

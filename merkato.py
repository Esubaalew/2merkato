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
                        'count': span_element.get_text(strip=True)[1:-1],
                        'businesses': get_businesses(DOMAIN + a_element['href'])
                    }

                    subcategory_list.append(subcategory_dict)

        return subcategory_list

    except Exception as e:
        logging.error(f"Error scraping {subcategory_url}: {e}")
        return []

def get_businesses(business_url):
    try:
        business_list = []

        while business_url:
            req = Request(business_url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(page, 'html.parser')

            businesses_div = soup.find('div', {'id': 'listings'})

            if businesses_div:
                for listing in businesses_div.find_all('div', {'class': 'span12 heading'}):
                    h4_element = listing.find('h4')
                    if h4_element:
                        a_element = h4_element.find('a')
                        business_detail_url = DOMAIN + a_element['href']
                        
            
                        business_details = get_business_details(business_detail_url)

                        business_dict = {
                            'name': a_element.get_text(strip=True),
                            'href': business_detail_url,
                            'details': business_details
                        }
                        business_list.append(business_dict)

                # Check for next page
                next_page = soup.find('a', {'title': 'Next'})
                if next_page:
                    business_url = DOMAIN + next_page['href']
                else:
                    business_url = None
            else:
                business_url = None

        return business_list

    except Exception as e:
        logging.error(f"Error scraping {business_url}: {e}")
        return []

def get_business_details(business_detail_url):
    try:
        req = Request(business_detail_url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')

        details_table = soup.find('table', {'class': 'table-condensed'})
        details_dict = {}

        if details_table:
            for row in details_table.find_all('tr'):
                columns = row.find_all('td')
                if len(columns) == 2:
                    key = columns[0].get_text(strip=True)
                    value = columns[1].get_text(strip=True)
                    details_dict[key] = value

        return details_dict

    except Exception as e:
        logging.error(f"Error scraping {business_detail_url}: {e}")
        return {}

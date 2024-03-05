from bs4 import BeautifulSoup
from urllib.request import urlopen
DOMAIN = 'https://www.2merkato.com'

def get_categories(url):
    page = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(page, 'html.parser')

    categories = soup.find_all('div', {'class': 'row-fluid mtree_category'})
    category_list = []

    for category in categories:
        a_element = category.find('a')
        span_element = category.find('span', {'class': 'count'})

        category_dict = {
            'name': a_element.get_text(strip=True),
            'href': DOMAIN + a_element['href'],
            'count': span_element.get_text(strip=True)[1:-1]
        }

        category_list.append(category_dict)

    return category_list

# 2merkato.py

"""
Scraping 2merkato Website for Business Information

This script scrapes business information from the 2merkato website, including categories, subcategories, businesses, and business details.
The scraped data is then saved to a CSV file and can be optionally converted to an Excel file.

Usage:
1. Adjust the constants like DOMAIN, URL, CSV_FILE_PATH, and EXCEL_FILE_PATH according to your needs.
2. Run the script to fetch data from the 2merkato website and save it to a CSV file.
3. Optionally, convert the CSV file to an Excel file using the provided function.

Note:
- Some details fetching (subcategories' businesses and business details) is commented out for performance reasons.
- Uncomment and adjust the code as needed for more comprehensive data.

Requirements:
- Python 3.x
- BeautifulSoup
- pandas
- requests

"""


from bs4 import BeautifulSoup
import logging
import requests
import pandas as pd
import csv
from typing import List, Dict, Optional

DOMAIN = 'https://www.2merkato.com'

def get_categories(directory_url: str = 'https://www.2merkato.com/directory/') -> List[Dict[str, str]]:
    """
    Fetch categories with details from the 2merkato website.

    Args:
        directory_url (str): The URL of the directory on the 2merkato website.
        
    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing category details (name, href, count, subcatagories(listofdict)).
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(directory_url, headers=headers)
        response.raise_for_status()  

        page = response.content.decode('utf-8', errors='replace')

        soup = BeautifulSoup(page, 'html.parser')

        categories = soup.find_all('div', {'class': 'row-fluid mtree_category'})

        category_list = []
        for category in categories:
            a_element = category.find_all('a')
            span_element = category.find_all('span', {'class': 'count'})

            for a, span in zip(a_element, span_element):
                category_dict = {
                    'name': a.get_text(strip=True),
                    'href': DOMAIN + a['href'],
                    'count': span.get_text(strip=True)[1:-1],
                    # 'subcategories': get_subcategories(DOMAIN + a_element['href']) [takes much time, so I commented it out.]
                }

                category_list.append(category_dict)

        return category_list

    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping {directory_url}: {e}")
        return []


def get_subcategories(category_url: str) -> List[Dict[str, str]]:
    """
    Fetch subcategories for a given category URL from the 2merkato website.

    Args:
        category_url (str): The URL of the category on the 2merkato website.
        
    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing subcategory details (name, href, count, bussiness[listofdict]).
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(category_url, headers=headers)
        response.raise_for_status() 

        page = response.content.decode('utf-8', errors='replace')

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
                        # 'businesses': get_businesses(DOMAIN + a_element['href']) [takes much time, so I commented it out.]
                    }

                    subcategory_list.append(subcategory_dict)

        return subcategory_list

    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping {category_url}: {e}")
        return []


def get_businesses(subcategory_url: str) -> List[Dict[str, str]]:
    """
    Fetch businesses for a given subcategory URL from the 2merkato website.

    Args:
        subcategory_url (str): The URL of the subcategory on the 2merkato website.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing business details (name, href, and details(dict)).
    """
    try:
        business_list = []
        business_url = subcategory_url 

        while business_url:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(business_url, headers=headers)
            response.raise_for_status() 

            page = response.content.decode('utf-8', errors='replace')

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
                            # 'details': business_details [takes much time, so I commented it out.]
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

    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping {subcategory_url}: {e}")
        return []

def get_business_details(business_url: str) -> Dict[str, str]:
    """
    Fetch details for a given business URL from the 2merkato website.

    Args:
        business_url (str): The URL of the business on the 2merkato website.

    Returns:
        Dict[str, str]: A dictionary containing business details extracted from the website.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(business_url, headers=headers)
        response.raise_for_status() 

        page = response.content.decode('utf-8', errors='replace')

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

    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping {business_url}: {e}")
        return {}


def scrape_to_csv(url: str = 'https://www.2merkato.com/directory/', csv_file_path: str = 'output.csv') -> None:
    """
    Scrape business data from the 2merkato website and write it to a CSV file.

    Args:
        url (str, optional): The URL of the directory on the 2merkato website. Defaults to 'https://www.2merkato.com/directory/'.
        csv_file_path (str, optional): The path to the CSV file. Defaults to 'output.csv'.
    """
    categories = get_categories(url)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Business Name', 'Subcategory', 'Category', 'Details'])

        for category in categories:  # you can use categories[:1] or any slicing to test the code with only one category to save time.
            print(f"Category: {category['name']}")
            subcategories = get_subcategories(category['href'])

            for subcategory in subcategories:
                print(f"  Subcategory: {subcategory['name']}")

                businesses = get_businesses(subcategory['href'])

                for business in businesses:
                    business_details = get_business_details(business['href'])

                    row_data = [
                        business['name'],
                        subcategory['name'],
                        category['name'],
                        str(business_details),
                    ]
                    csv_writer.writerow(row_data)

    print(f"CSV file '{csv_file_path}' created successfully.")


def convert_csv_to_excel(csv_file_path: str, excel_file_path: str) -> None:
    """
    Convert a CSV file to an Excel file.

    Args:
        csv_file_path (str): The path to the input CSV file.
        excel_file_path (str): The path to the output Excel file.

    Returns:
        None
    """
    df = pd.read_csv(csv_file_path)
    df.to_excel(excel_file_path, index=False)

    print(f"Excel file '{excel_file_path}' created successfully.")



if __name__ == "__main__":
    scrape_to_csv()
    convert_csv_to_excel('output.csv', 'output.xlsx')

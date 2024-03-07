# 2merkato Scraper

## Overview

This Python script scrapes business information from the 2merkato website, including categories, subcategories, businesses, and business details. The scraped data can be saved to a CSV file and optionally converted to an Excel file.

## Usage

1. Install the required libraries:
    ```bash
    pip install beautifulsoup4 pandas requests
    ```

2. Run the script:
    ```bash
    python 2merkato.py
    ```


## Requirements

- Python 3.x
- BeautifulSoup
- pandas
- requests

## Script Structure

- `get_categories`: Fetches categories with details from the 2merkato website.
- `get_subcategories`: Fetches subcategories for a given category URL.
- `get_businesses`: Fetches businesses for a given subcategory URL.
- `get_business_details`: Fetches details for a given business URL.
- `scrape_to_csv`: Scrapes business data and writes it to a CSV file.
- `convert_csv_to_excel`: Converts a CSV file to an Excel file.
- `main`: entry point.


## Note

- Some details fetching is commented out for performance reasons. Uncomment and adjust the code for more comprehensive data.

## Example

```bash
# Run the script to fetch data and save to a CSV file
python 2merkato.py

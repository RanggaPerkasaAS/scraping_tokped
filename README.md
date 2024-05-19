Overview
This Python script uses Selenium and BeautifulSoup to scrape product data from Tokopedia's search results for Samsung phones. The script navigates to the search results page, scrolls through the listings to load more items, and then extracts relevant information (product name, price, number of items sold, and product link). Finally, the data is saved into an Excel file.

Requirements
To run this script, you need to have the following installed:

Python 3.x
Selenium
BeautifulSoup4
pandas
openpyxl
ChromeDriver
Installation
Step 1: Install Python Packages
You can install the required Python packages using pip:

bash
1.Copy code
2.pip install selenium
3.pip install beautifulsoup4
4.pip install pandas
5.pip install openpyxl
6.Step 2: Download ChromeDriver

Download the appropriate version of ChromeDriver for your Chrome browser from the ChromeDriver download page. Place the chromedriver.exe file in the same directory as your script or add its path to your system's PATH environment variable.

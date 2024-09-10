from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize the ChromeOptions
options = webdriver.ChromeOptions()
# Uncomment the line below to run headless (without opening a browser window)
# options.add_argument("--headless")  
driver = webdriver.Chrome(options=options)

shop_links = []

# Iterate through multiple pages (adjust the range as necessary)
for j in range(1, 29):
    link = f"https://www.tokopedia.com/official-store/brand/fashion/?page={j}"
    driver.get(link)
    
    # Wait until the product listings are present
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-14f1oi')))

    # Scroll to load more content
    for i in range(1, 5):
        driver.execute_script(f"window.scrollTo(0, {500 * i})")
        print(f"Scrolling {i} times")
        time.sleep(1)

    # Get page source after loading content
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Find all the brand links within the desired container
    brand_links = soup.find_all('a', {'data-testid': 'lblOSBrandLink'})

    # Extract the href attribute from each link
    for link in brand_links:
        href = link['href']
        print(f"Found link: {href}")
        shop_links.append(href)

# Now, collect details for each shop link (if needed)
data_brands = []

for shop_link in shop_links:
    driver.get(shop_link)

    try :
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-fzzhh3')))

        content_brand = driver.page_source
        soup_brand = BeautifulSoup(content_brand, 'html.parser')
        
        brand_name = soup_brand.find('h1', class_='css-fzzhh3')
        brand_address = soup_brand.find('span', {'data-testid': 'shopLocationHeader'})
        
        data_brands.append({
            'brand_name': brand_name.get_text() if brand_name else None,
            'brand_address': brand_address.get_text() if brand_address else None,
            'brand_category': 'Fashion'
        })
    
    except TimeoutException:
        print(f"Timeout occurred while loading shop link: {shop_link}. Continuing to the next link.")
        continue

# Save the extracted data to an Excel file
df = pd.DataFrame(data_brands)
df.to_excel('Tokped_Fashion_brand.xlsx', sheet_name='Sheet1', index=False)

# Close the browser
driver.quit()

print("Data scraping and saving to Excel completed successfully.")

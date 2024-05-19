from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup;
import pandas as pd;
import time;

option = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
option.add_experimental_option("prefs",prefs)
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=option)

link = "https://www.tokopedia.com/search?q=hp+samsung&source=universe&st=product&navsource=home&srp_component_id=02.02.02.01"

driver.get(link)
# Wait until the product listings are present
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-llwpbs')))

rentang = 500
for i in range(1, 13):
    akhir = rentang * i
    perintah = f"window.scrollTo(0, {akhir})"
    driver.execute_script(perintah)
    print(f"loading ke-{i}")
    time.sleep(1)

content = driver.page_source

data = BeautifulSoup(content,'html.parser')

data_barang = []

i=1
for area in data.find_all('div',class_="css-llwpbs"):
    print("proses add " + str(i))
    nama_barang = area.find('div', class_="prd_link-product-name css-3um8ox")
    harga_barang = area.find('div', class_="prd_link-product-price css-h66vau")
    terjual = area.find('span', class_="prd_label-integrity css-1sgek4h")
    link_barang = area.find('a')['href']
    if nama_barang != None:
        nama_barang = nama_barang.get_text()
    if harga_barang != None:
        harga_barang = harga_barang.get_text()
    if terjual != None:
        terjual = terjual.get_text()
    if link_barang != None:
        link_barang = link_barang
    
    i+=1
    
    data_barang.append({
        'nama' : nama_barang,
        'harga' : harga_barang,
        'terjual' : terjual,
        'link barang' : link_barang,
    })

driver.quit()


df = pd.DataFrame(data_barang)
with pd.ExcelWriter('tokped.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)
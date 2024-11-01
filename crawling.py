from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote, unquote
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

set_url_list_joongonara =set()

def joongonaraGetUrl(page):
    for i in range(page):
        url = 'https://web.joongna.com/search?category=158&page='+str(i+1)
        driver.get(url)
        
        try:
            items = driver.find_elements(By.XPATH, "/html/body/div/div/main/div[1]/div/ul[2]/li/a")


            for item in items:
                url = item.get_attribute("href")
                if url.startswith("https://web"):  # URL이 "https://web"으로 시작하는지 확인 -> 중고나라에 광고 url 이 껴있는데 https://web 으로 시작하지 않음
                    set_url_list_joongonara.add(url)
            
        finally:
            time.sleep(1)
                
    for url in set_url_list_joongonara:
        driver.get(url)
        time.sleep(1)

        try:
            title = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[1]/div[2]/div[2]/div[1]/h1").text
            content = driver.find_element(By.XPATH,"/html/body/div/div/main/div[1]/div[3]/div[1]/div/div/article/p").text
        finally:
            print(title)
            print(content)
            print("끝")
    driver.quit()


joongonaraGetUrl(1)

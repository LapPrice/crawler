from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote, unquote
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


def joongonaraGetUrl(page_number):
    url = 'https://web.joongna.com/search/노트북?page='+str(page_number)
    driver.get(url)
    
    try:
        items = driver.find_elements(By.XPATH, "/html/body/div/div/main/div[1]/div/ul[2]/li/a")

        valid_links = []

        for item in items:
            url = item.get_attribute("href")
            if url.startswith("https://web"):  # URL이 "https://web"으로 시작하는지 확인
                valid_links.append(url)
        
        set_list = set(valid_links)

        for url in set_list:
            print(url)

    finally:
        # 4. 드라이버 종료
        time.sleep(2)
        driver.quit()


joongonaraGetUrl(1)

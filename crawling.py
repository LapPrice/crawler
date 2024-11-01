from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote, unquote
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

set_url_list_joongonara =set()

def joongonaraGetUrl():
    for i in range(5):
        url = 'https://web.joongna.com/search/노트북?page='+str(i+1)
        driver.get(url)
        
        try:
            items = driver.find_elements(By.XPATH, "/html/body/div/div/main/div[1]/div/ul[2]/li/a")


            for item in items:
                url = item.get_attribute("href")
                if url.startswith("https://web"):  # URL이 "https://web"으로 시작하는지 확인
                    set_url_list_joongonara.add(url)
            
        finally:
            # 4. 드라이버 종료
            time.sleep(1)
    driver.quit()
    for url in set_url_list_joongonara:
            print(url)
    print("끝")



joongonaraGetUrl()
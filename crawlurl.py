from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time



service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def crawlURL(page,file_path):
    recorded_urls = read_urls_from_file(file_path)

    for i in range(page):
            url = 'https://web.joongna.com/search?category=158&page='+str(i+1) #category=158에서 랩탑에 대한 것들만 검색 가능함
            driver.get(url)          
            # wait = WebDriverWait(driver, 20)
            # wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))
            time.sleep(1.5)
            try:
                items = driver.find_elements(By.XPATH, "/html/body/div/div/main/div[1]/div/ul[2]/li/a")
                
                for item in items:
                    url = item.get_attribute("href")
                    if url.startswith("https://web") and url not in recorded_urls:  # URL이 "https://web"으로 시작하는지 확인 -> 중고나라에 광고 url 이 껴있는데 https://web 으로 시작하지 않음
                        append_url_to_file(url,file_path)            
            finally:
                time.sleep(1)



def read_urls_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())  # 파일에서 URL을 읽어 집합(set)으로 반환
    except FileNotFoundError:
        return set()
    

# 새로운 URL을 파일에 추가하는 함수
def append_url_to_file(url, file_path):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(url + "\n")  # 새로운 URL을 파일에 추가

# Selenium을 사용하여 웹 페이지에서 URL을 크롤링하는 함수
def crawl_url_with_selenium(start_url, file_path):
    # 이미 기록된 URL들 읽기
    recorded_urls = read_urls_from_file(file_path)
    
    # 페이지가 완전히 로드될 때까지 대기 (필요시)
    time.sleep(1)  # 페이지가 로드되는데 충분한 시간 (필요에 따라 조정)

    # 모든 링크(a 태그) 찾기
    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        url = link.get_attribute('href')  # 링크에서 href 속성 가져오기
        if url and url not in recorded_urls:
            print(f"Crawling and saving URL: {url}")
            append_url_to_file(url, file_path)  # 새로운 URL 파일에 기록
            recorded_urls.add(url)  # 기록된 URL에 추가
        else:
            print(f"Skipping already recorded URL: {url}")

    driver.quit()  # 드라이버 종료

file_path = 'crawl_url_from_joongonara.txt'  # 기록할 URL 파일 경로
crawlURL(100, file_path)
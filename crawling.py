from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from openai import OpenAI
import json


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

json_file_name = "gpt_response.json"

set_url_list_joongonara =set()

def getJoongonara(page):
    for i in range(page):
        url = 'https://web.joongna.com/search?category=158&page='+str(i+1) #category=158에서 랩탑에 대한 것들만 검색 가능함
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
            price = driver.find_element(By.XPATH,"/html/body/div/div/main/div[1]/div[1]/div[2]/div[2]/div[2]/div").text
        finally:
            to_response = title+content+price
            request_to_gpt(to_response)

    driver.quit()


def request_to_gpt(request):
    with open("gptkey.txt","r",encoding="utf-8") as file:
        key=file.read()

    client = OpenAI(api_key=key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
        {"role": "system", "content": "내가 지금부터 본문을 전해줄테니까 이제 output을 json으로 해줘"},
        {"role":"system","content":
        """
            내가 지금부터 노트북 판매 게시글의 본문 내용을 줄건데, 내용으로부터 다음 값들을 추출해줘. 
        반환값은 Json으로 해주고, Scheme은 다음과 같아.
        {
            name : String |undefined
            brand : 'SAMSUNG' | 'LG' | 'APPLE' | 'MSI' | 'ASUS' | 'DELL' |'HP'|'HANSUNG'|' MS'| 
            'ACER' |'ALLDOCUBE'|'BASICS'|'CHUWI'|'DICLE'|'FORYOUDIGITAL'|'GIGABYTE'|'GPD'|'HP'|'HUAWEI'|'JOOYON'|'LENOVO'
            |'MPGIO'|'NEXTBOOK'|'RAZER'|'TEDAST'|'VICTRACK' |'unknown';
            CPU : string |
            RAM : number | undefined;
            INCH : number | undefined; 
            DISK : number | undefined;
            GPU : 'external'|'internal'; 
            weight : number | undefined;
            price: number| undefined;
        }
        """ },
        {"role": "user", "content": request }
        ],
        max_tokens=100
    )
    response_data = response.choices[0].message['content']

    # JSON 파일로 저장
    with open(json_file_name, "a", encoding="utf-8") as file:
        json.dump(response_data, file, ensure_ascii=False, indent=4)


getJoongonara(1)


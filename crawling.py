from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from openai import OpenAI
import json 
import os


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
            request_to_gpt(to_response,url)
    
    close_json_file()
    driver.quit()


def request_to_gpt(request,url):
    with open("gptkey.txt","r",encoding="utf-8") as file:
        key=file.read()

    client = OpenAI(api_key=key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
        {"role": "system", "content": "if CPU manufacturer is Intel, parse it like this : example(i5-8250U OR Ultra-5 OR Pentium-N3700)"},
        {"role": "system", "content": "If the CPU manufacturer is Apple, parse it like this: example (M-8 OR M3-Pro-11 OR M3-Max-16)."},
        {"role": "system", "content": "If the CPU manufacturer is AMD , parse it like this: example (Ryzen-5-7520U)."},
        {"role": "system", "content": "Please respond in Korean."},


        {"role":"system","content":

        """
        I will give you the content of a laptop sales post, and from that content, please extract the following values. 
        Return the values in JSON format, and the scheme is as follows.
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
            price: number| undefined;
            url:url|undefined;
        }
        """ },
        {"role": "user", "content": request }
        ],
    )
    response_data = response.choices[0].message.content
    
    try:
        # response_data가 문자열 형태의 JSON이면 이를 파싱하여 Python 딕셔너리로 변환
        response_dict = json.loads(response_data)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return
    
    response_dict["url"] = url
    append_to_json_file(response_dict)
    
            
def append_to_json_file(data):
    with open(json_file_name, "a", encoding="utf-8") as file:
        if file.tell() == 0:  # 파일이 비어 있으면 배열 시작
            file.write("[\n")
        else:  # 파일에 내용이 있으면 쉼표 추가
            file.write(",\n")
        
        json.dump(data, file, ensure_ascii=False, indent=4)

def close_json_file():
    with open(json_file_name, "rb+") as file:
        file.seek(-1, os.SEEK_END)  # 마지막 쉼표 위치로 이동
        file.truncate()  # 쉼표 제거
        file.write(b"\n]")  # 배열 닫기


getJoongonara(1)

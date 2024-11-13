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

def getJoongonara(file_path):
    with open("gptkey.txt","r",encoding="utf-8") as file:
        key=file.read()

    recorded_urls = read_urls_from_file(file_path)
    
    for url in recorded_urls:
        driver.get(url)
        try:
            title = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[1]/div[2]/div[2]/div[1]/h1").text
            content = driver.find_element(By.XPATH,"/html/body/div/div/main/div[1]/div[3]/div[1]/div/div/article/p").text
            price = driver.find_element(By.XPATH,"/html/body/div/div/main/div[1]/div[1]/div[2]/div[2]/div[2]/div").text
        finally:
            to_response = title+content+price
            response_dict = request_to_gpt(key,to_response)
            response_dict["url"] = url
            append_to_json_file(response_dict,"gpt_response.json")
            time.sleep(1)
    driver.quit()


    


def request_to_gpt(key,request):
    

    client = OpenAI(api_key=key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
        {"role": "system", "content": "if CPU manufacturer is Intel, parse it like this : example(i5-8250U OR Ultra-5 OR Pentium-N3700)"},
        {"role": "system", "content": "If the CPU manufacturer is Apple, parse it like this: example (M-8 OR M3-Pro-11 OR M3-Max-16 OR M2)."},
        {"role": "system", "content": "If the CPU manufacturer is AMD , parse it like this: example (Ryzen-5-7520U)."},
        {"role": "system", "content": "If the CPU manufacturer is AMD , parse it like this: example (Ryzen-5-7520U)."},
        {"role": "system", "content": """
         I'm a software developer, and I need standardized data values to store in a database. 
         I'll give you a few examples, and please respond in the same way:"그램" -> "Gram", "맥북에어" -> "MacBookAir", "이온" -> "Ion", "갤럭시북2프로" -> "GalaxyBook2Pro". 
         Laptop model names need to be standardized like this.
         """},
        {"role":"system","content":

        """
        I will give you the content of a laptop sales post, and from that content, please extract the following values. 
        Return the values in JSON format, and the scheme is as follows.
        {
            name : String |undefined ; 
            brand : 'SAMSUNG' | 'LG' | 'APPLE' | 'MSI' | 'ASUS' | 'DELL' |'HP'|'HANSUNG'|' MS'| 
            'ACER' |'ALLDOCUBE'|'BASICS'|'CHUWI'|'DICLE'|'FORYOUDIGITAL'|'GIGABYTE'|'GPD'|'HP'|'HUAWEI'|'JOOYON'|'LENOVO'
            |'MPGIO'|'NEXTBOOK'|'RAZER'|'TEDAST'|'VICTRACK' |'undefined';
            CPU : string | undefined;
            RAM : number | undefined;
            INCH : number | undefined; // INCH must be a INTEGER number 
            DISK : number | undefined;
            price: number| undefined;
            url:url|undefined;
        }
        """ },
        {"role": "user", "content": request }
        ],
    )
    response_data = response.choices[0].message.content
    try:
        response_dict = json.loads(response_data)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return
    
    return response_dict
    
def append_to_json_file(data, file_path):
    try:
        # JSON 파일 읽기
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []  # 파일이 없으면 빈 배열로 초기화
        
        # 새 데이터 추가
        if isinstance(existing_data, list):
            existing_data.append(data)
        else:
            print("JSON 구조가 배열이 아닙니다.")
            return
        
        # 파일에 저장
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 오류: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")


def read_urls_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())  # 파일에서 URL을 읽어 집합(set)으로 반환
    except FileNotFoundError:
        return set()
    

getJoongonara("crawl_url_from_joongonara.txt")



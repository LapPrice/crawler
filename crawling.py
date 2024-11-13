from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

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
        time.sleep(2)
        try:
            try:
                title = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[1]/div[2]/div[2]/div[1]/h1").text
            except NoSuchElementException:
                continue
            try:
                content = driver.find_element(By.XPATH,"/html/body/div/div/main/div[1]/div[3]/div[1]/div/div/article/p").text
            except NoSuchElementException:
                continue
            try:
                price = driver.find_element(By.XPATH,"/html/body/div/div/main/div[1]/div[1]/div[2]/div[2]/div[2]/div").text
            except NoSuchElementException:
                continue
        finally:
            to_response = title+content+price
            response_dict = request_to_gpt(key,to_response)
            response_dict["URL"] = url
            if(response_dict["ram"]==None or 0) :continue #ram 이 null 이면 pass 
            if(response_dict["name"]=="undefined") :continue #ram 이 null 이면 pass 
            if(response_dict["cpu"]=="undefined") :continue #cpu 가 undefined 면 pass
            if(response_dict["brand"]=="undefined") :continue
            if(response_dict["brand"]==response_dict["name"]) : continue # name 과 브랜드가 같으면 패스
            append_to_json_file(response_dict,"gpt_response.json")
    driver.quit()


    


def request_to_gpt(key,request):
    

    client = OpenAI(api_key=key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
        {"role": "system", "content": "if CPU manufacturer is Intel, parse it like this : example that i want('i5-8250U' OR (give me 'Ultra-5' not 'Ultra-5-125H' it shpuld be 'Ultra-5') OR 'Pentium-N3700')"},
        {"role": "system", "content": "If the CPU manufacturer is Apple, parse it like this: example (M-8 OR M3-Pro-11 OR M3-Max-16 OR M2)."},
        {"role": "system", "content": "If the CPU manufacturer is AMD , parse it like this: example (Ryzen-5-7520U)."},
        {"role": "system", "content": "Please respond without any spaces."},
        {"role" : "system", "content": "The JSON key 'name' should be english"},
        {"role": "system", "content":
        """
         I'm a software developer, and I need standardized data values to store in a database. 
         Laptop model names need to be standardized like this
        """},
         {"role":"system","content":
          """
          When you find the word "그램," please only translate it as "Gram." and Please format it as "Gram" not "Gram14"
          Also, "이온" should be "Ion," "갤럭시북" should be "GalaxyBook,"also it should be "GalaxyBook" 
          and "맥북"  "MacBook." but it can permit "MacBookAir" or "MacBookPro" and Please format it as "MacBookPro," not "MacBookPro16"
           For the rest of the names, you can translate them as you see fit.
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
            cpu : string | undefined;
            ram : number | undefined;
            inch : number | undefined; // inch must be a INTEGER number 
            disk : number | undefined;
            price: number| undefined;
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
                content = file.read().strip()
                # 파일이 비어있거나 JSON 형식이 아닌 경우 처리
                if content:
                    existing_data = json.loads(content)
                else:
                    existing_data = []
        except FileNotFoundError:
            existing_data = []  # 파일이 없으면 빈 배열로 초기화
        except json.JSONDecodeError:
            existing_data = []  # 잘못된 JSON 형식이면 빈 배열로 초기화

        # 새 데이터 추가
        if isinstance(existing_data, list):
            existing_data.append(data)
        else:
            print("JSON 구조가 배열이 아닙니다.")
            return
        
        # 파일에 저장
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"오류 발생: {e}")

def read_urls_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())  # 파일에서 URL을 읽어 집합(set)으로 반환
    except FileNotFoundError:
        return set()
    

getJoongonara("crawl_url_from_joongonara.txt")



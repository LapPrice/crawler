import threading
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

def create_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver


def get_danawa(file_path):
    driver = create_driver()
    try:
        with open("gptkey.txt", "r", encoding="utf-8") as file:
            key = file.read()

        recorded_urls = read_urls_from_file(file_path)

        for url in recorded_urls:
            driver.get(url)
            time.sleep(2)
            try:
                title = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/p[1]").text
                contents = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]")
                content = " ".join([content.text for content in contents])
                price = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/p[2]/span").text
                to_response = title + content + price
                response_dict = request_to_gpt(key, to_response)
                process_response(response_dict, "다나와", url)
            except NoSuchElementException:
                continue
    finally:
        driver.quit()


def get_joongo(file_path):
    driver = create_driver()
    try:
        with open("gptkey.txt", "r", encoding="utf-8") as file:
            key = file.read()

        recorded_urls = read_urls_from_file(file_path)

        for url in recorded_urls:
            driver.get(url)
            time.sleep(2)
            try:
                title = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[1]/div[2]/div[2]/div[1]/h1").text
                content = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[3]/div[1]/div/div/article/p").text
                price = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[1]/div[2]/div[2]/div[2]/div").text
                to_response = title + content + price
                response_dict = request_to_gpt(key, to_response)
                process_response(response_dict, "중고나라", url)
            except NoSuchElementException:
                continue
    finally:
        driver.quit()

def request_to_gpt(key,request):
    

    client = OpenAI(api_key=key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
        {"role": "system", "content": "if CPU manufacturer is Intel, parse it like this : example that i want('i5-8250U' OR (give me 'Ultra-5' not 'Ultra-5-125H' it shpuld be 'Ultra-5') OR 'Pentium-N3700')"},
        {"role": "system", "content": "If the CPU manufacturer is Apple, parse it like this: example (M1 OR M3 Pro OR M3 Max OR M2, OR M2 Pro). please give me just M1, M2, M3, M1 Pro,M2 Pro,M3 Pro,M3 Max"},
        {"role": "system", "content": "Remove the all of parentheness, and if cpu name has only frequency or too simplified name (ex. ONLY i5 OR 2.6ghz OR i5-4세대 or i5-13th ), cpu name should be undefined.  "},
        {"role": "system", "content": "If the CPU manufacturer is AMD , parse it like this: example (Ryzen-5-7520U)."},
        {"role": "system", "content": "If ssd marked 1TB give me data as 1024"},
        {"role" : "system", "content": "Json key 'cpu' should contain only english and also i5-7세대, i-5 7th litke this pattern should be the i5 "},
        {"role" : "system", "content": "The JSON key 'name' and 'cpu' should be english"},
        {"role" : "system", "content": "The key value 'name' in JSON should not allow spaces And also, remove the model name at the end."},
        {"role" : "system", "content": "The key value name in JSON should not allow spaces."},
        {"role" : "system", "content": "If spaces are included, replace them with hyphens (`-`).like UltraPC-> Ultra-PC"},
        
        {"role": "system", "content":
        """
         I'm a software developer, and I need standardized data values to store in a database. 
         Laptop model names need to be standardized like this
        """},
         {"role":"system","content":
          """
          When you find the word "그램," please only translate it as "Gram." and Please format it as "Gram" not "Gram14" ,"Gram15" Gram16",and "Gram17" 
          Also, "이온" should be "Ion," "갤럭시북" should be "GalaxyBook,"also it should be "GalaxyBook" 
          and "맥북"  "MacBook." but it can permit "MacBookAir" or "MacBookPro" and Please format it as "MacBookPro," not "MacBookPro16"
           For the rest of the names, you can translate them as you see fit.
          """},
        {"role":"user","content":

        """
        I will give you the content of a laptop sales post, and from that content, please extract the following values. 
        Return the values in JSON format, and the scheme is as follows.
        {
            name : String |undefined ; 
            brand : 'SAMSUNG' | 'LG' | 'APPLE' | 'MSI' | 'ASUS' | 'DELL' |'HP'|'HANSUNG'|' MS'| 
            'ACER' |'ALLDOCUBE'|'BASICS'|'CHUWI'|'DICLE'|'FORYOUDIGITAL'|'GIGABYTE'|'GPD'|'HP'|'HUAWEI'|'JOOYON'|'LENOVO'
            |'MPGIO'|'NEXTBOOK'|'RAZER'|'TEDAST'|'VICTRACK' |'undefined';
            cpu : string | undefined;
            ram : number | null;
            inch : number | undefined; // inch should be 0 and should Integer if you can't find inch number
            ssd : number | null;
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


def get_bunjang(file_path):
    driver = create_driver()
    try:
        with open("gptkey.txt", "r", encoding="utf-8") as file:
            key = file.read()

        recorded_urls = read_urls_from_file(file_path)

        for url in recorded_urls:
            driver.get(url)
            time.sleep(2)
            try:
                title = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[1]").text
                content = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div[1]/div/div[5]/div[1]/div/div[1]/div[2]/div[1]/p").text
                price = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div").text
                to_response = title + content + price
                response_dict = request_to_gpt(key, to_response)
                process_response(response_dict, "번개장터", url)
            except NoSuchElementException:
                continue
    finally:
        driver.quit()


def process_response(response_dict, source, url):
    response_dict["URL"] = url
    response_dict["source"] = source

    try:
        # "ram" 키 확인 및 값 검증
        if response_dict.get("ram") in (None, 0, "undefined"):
            raise NoSuchElementException
    except NoSuchElementException as e:
        return  # 현재 데이터 무시하고 다음으로 진행
    except KeyError as e:  # 키 자체가 없을 경우
        raise NoSuchElementException

    if response_dict["ram"] in (None, 0, "undefined"):
        raise NoSuchElementException
    if response_dict["name"] in "undefined":
        raise NoSuchElementException
    if response_dict["inch"] in (None, 0, "undefined"):
        raise NoSuchElementException
    if response_dict["cpu"] in "undefined":
        raise NoSuchElementException
    if response_dict["brand"] in "undefined":
        raise NoSuchElementException
    if response_dict["ssd"] in (None, 0, "undefined"):
        raise NoSuchElementException
    if response_dict.get("brand", "").lower() == response_dict.get("name", "").lower():
        raise NoSuchElementException
    if response_dict["price"] in (None,0,"undefined"):
        raise NoSuchElementException
    if response_dict["name"] in "undefined":
        raise NoSuchElementException
    
   
    
    append_to_json_file(response_dict, "gpt_response.json")


def append_to_json_file(data, file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)


def read_urls_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()


# 멀티스레드 실행
joongo_thread = threading.Thread(target=get_joongo, args=("crawl_url_from_joongonara.txt",))
bunjang_thread = threading.Thread(target=get_bunjang, args=("crawl_url_from_bunjang.txt",))

# 스레드 시작
joongo_thread.start()
bunjang_thread.start()

# 스레드 종료 대기
joongo_thread.join()
bunjang_thread.join()

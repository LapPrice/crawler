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


# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

json_file_name = "gpt_response.json"

def get_danawa(file_path):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    with open("gptkey.txt", "r", encoding="utf-8") as file:
        key = file.read()

    recorded_urls = read_urls_from_file(file_path)

    for url in recorded_urls:
        driver.get(url)
        time.sleep(2)
        try:
            try:
                title = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/p[1]").text
            except NoSuchElementException:
                continue
            try:
                contents = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[2]")
                content = " ".join([content.text for content in contents])
            except NoSuchElementException:
                continue
            try:
                price = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/p[2]/span").text
            except NoSuchElementException:
                continue
        finally:
            to_response = title + content + price
            response_dict = request_to_gpt(key, to_response)
            try:
                response_dict["URL"] = url
                response_dict["source"] = "다나와"
                if response_dict["ram"] in (None, 0, "undefined"): continue
                if response_dict["name"] in "undefined": continue
                if response_dict["inch"] in (None, 0, "undefined"): continue
                if response_dict["cpu"] in "undefined": continue
                if response_dict["brand"] in "undefined": continue
                if response_dict["ssd"] in (None, 0, "undefined"): continue
                if response_dict["brand"] == response_dict["name"]: continue
                append_to_json_file(response_dict, "gpt_response.json")
            except Exception:
                print("Error occurred while parsing.")
                continue
    driver.quit()

def get_joongo(file_path):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    with open("gptkey.txt", "r", encoding="utf-8") as file:
        key = file.read()

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
                content = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[3]/div[1]/div/div/article/p").text
            except NoSuchElementException:
                continue
            try:
                price = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[1]/div[2]/div[2]/div[2]/div").text
            except NoSuchElementException:
                continue
        finally:
            to_response = title + content + price
            response_dict = request_to_gpt(key, to_response)
            try:
                response_dict["URL"] = url
                response_dict["source"] = "중고나라"
                if response_dict["ram"] in (None, 0, "undefined"): continue
                if response_dict["name"] in "undefined": continue
                if response_dict["inch"] in (None, 0, "undefined"): continue
                if response_dict["cpu"] in "undefined": continue
                if response_dict["brand"] in "undefined": continue
                if response_dict["ssd"] in (None, 0, "undefined"): continue
                if response_dict["brand"] == response_dict["name"]: continue
                append_to_json_file(response_dict, "gpt_response.json")
            except Exception:
                print("Error occurred while parsing.")
                continue
    driver.quit()
def get_bunjang(file_path):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    with open("gptkey.txt", "r", encoding="utf-8") as file:
        key = file.read()

    recorded_urls = read_urls_from_file(file_path)

    for url in recorded_urls:
        driver.get(url)
        time.sleep(2)
        try:
            try:
                title = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[1]").text
            except NoSuchElementException:
                continue
            try:
                content = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div[1]/div/div[5]/div[1]/div/div[1]/div[2]/div[1]/p").text
            except NoSuchElementException:
                continue
            try:
                price = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div").text
            except NoSuchElementException:
                continue
        finally:
            to_response = title + content + price
            response_dict = request_to_gpt(key, to_response)
            try:
                response_dict["URL"] = url
                response_dict["source"] = "번개장터"
                if response_dict["ram"] in (None, 0, "undefined"): continue
                if response_dict["name"] in "undefined": continue
                if response_dict["inch"] in (None, 0, "undefined"): continue
                if response_dict["cpu"] in "undefined": continue
                if response_dict["brand"] in "undefined": continue
                if response_dict["ssd"] in (None, 0, "undefined"): continue
                if response_dict["brand"] == response_dict["name"]: continue
                append_to_json_file(response_dict, "gpt_response.json")
            except Exception:
                print("Error occurred while parsing.")
                continue
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
        {"role": "system", "content": "your respone key to value cpu name should be simplified also cannot contain korean just english please"},
        {"role": "system", "content": "If ssd marked 1TB give me data as 1024"},
        {"role" : "system", "content": "The JSON key 'name' and 'cpu' should be english"},
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
    





get_danawa("crawl_url_from_danawa.txt")
get_bunjang("crawl_url_from_bunjang.txt")
get_joongo("crawl_url_from_joongonara.txt")



if __name__ == "__main__":
    danawa_thread = threading.Thread(target=get_danawa, args=("crawl_url_from_danawa.txt",))
    joongo_thread = threading.Thread(target=get_joongo, args=("crawl_url_from_joongonara.txt",))
    bunjang_thread = threading.Thread(target=get_bunjang, args=("crawl_url_from_bunjang.txt",))

    danawa_thread.start()
    joongo_thread.start()
    bunjang_thread.start()

    danawa_thread.join()
    joongo_thread.join()
    bunjang_thread.join()

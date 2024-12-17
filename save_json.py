import requests
import json

with open("gpt_response.json", "r",encoding="utf-8") as file:
    data = json.load(file)

    # 백엔드 API로 데이터 전송 현재는 로컬
response = requests.post("http://43.203.181.135:8080/api/laptop/laptops", json=data)

# 결과 출력``
print(response.status_code)
print(response.text)
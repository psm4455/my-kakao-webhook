import requests

url = "http://127.0.0.1:5000"
data = {
    "message": "📉 RSI 과매도! 진입 타점 확인 요망"
}

response = requests.post(url, json=data)

print("응답 코드:", response.status_code)
print("응답 내용:", response.json())

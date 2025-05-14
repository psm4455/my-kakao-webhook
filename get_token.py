import requests

# 카카오 토큰 요청 URL
url = "https://kauth.kakao.com/oauth/token"

# POST 요청에 사용할 데이터
data = {
    "grant_type": "authorization_code",
    "client_id": "f37a2090d8a668183699437f586bf241",  # 앱 REST API 키
    "redirect_uri": "https://my-kakao-webhook.onrender.com",  # 등록한 리디렉션 URI
    "code": "0XiMuybFRZBIfF7EBEyP6o98Gr3IMVovXIlxCsqmgX8Zcd9gSzYoGAAAAAQKFxTuAAABls-QXK22W8wW6V7rJg"  # 발급받은 인가 코드
}

# POST 요청 보내기
response = requests.post(url, data=data)

# 결과 출력
print(response.json())
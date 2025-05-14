from flask import Flask, request
import requests
import json
import os
import time

app = Flask(__name__)

# 파일에 저장된 토큰 불러오기
def load_tokens():
    if not os.path.exists("tokens.json"):
        return None
    with open("tokens.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 파일에 토큰 저장하기
def save_tokens(tokens):
    with open("tokens.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f)

# 액세스 토큰 만료 시 자동 갱신
def refresh_access_token(refresh_token):
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": "f37a2090d8a668183699437f586bf241",
        "refresh_token": refresh_token
    }
    response = requests.post(url, data=data)
    new_tokens = response.json()
    print("🔄 리프레시 성공:", new_tokens)

    tokens = load_tokens()
    if "access_token" in new_tokens:
        tokens["access_token"] = new_tokens["access_token"]
    if "refresh_token" in new_tokens:
        tokens["refresh_token"] = new_tokens["refresh_token"]
    save_tokens(tokens)
    return tokens["access_token"]

# 카카오톡으로 메시지 보내기
def send_kakao_message(msg):
    tokens = load_tokens()
    access_token = tokens["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": msg,
            "link": {
                "web_url": "https://www.naver.com"
            },
            "button_title": "확인"
        })
    }

    response = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers=headers, data=data
    )

    # 만약 액세스 토큰이 만료되었을 경우
    if response.status_code == 401:
        print("⛔ 토큰 만료됨. 갱신 시도...")
        new_token = refresh_access_token(tokens["refresh_token"])
        headers["Authorization"] = f"Bearer {new_token}"
        response = requests.post(
            "https://kapi.kakao.com/v2/api/talk/memo/default/send",
            headers=headers, data=data
        )

    return response.text

# 웹훅 엔드포인트
@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        data = request.json
        message = data.get("message", "기본 메시지입니다.")
        result = send_kakao_message(message)
        return result
    else:
        return "✅ 카카오톡 웹훅 서버 작동 중!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

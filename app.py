from flask import Flask, request, jsonify
import requests
import json
import time

app = Flask(__name__)

# 환경 설정
KAKAO_REST_API_KEY = "f37a2090d8a668183699437f586bf241"
KAKAO_REDIRECT_URI = "https://my-kakao-webhook.onrender.com"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
TOKENS_FILE = "tokens.json"

# ✅ 토큰 파일 읽기
def load_tokens():
    with open(TOKENS_FILE, "r") as f:
        return json.load(f)

# ✅ 토큰 파일 저장
def save_tokens(tokens):
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f)

# ✅ 토큰 만료 체크 후 자동 갱신
def get_valid_access_token():
    tokens = load_tokens()
    now = int(time.time())

    if now >= tokens.get("expires_at", 0):
        print("🔄 엑세스 토큰이 만료되어 갱신합니다...")
        refresh_data = {
            "grant_type": "refresh_token",
            "client_id": KAKAO_REST_API_KEY,
            "refresh_token": tokens["refresh_token"]
        }
        response = requests.post(KAKAO_TOKEN_URL, data=refresh_data)
        if response.status_code == 200:
            new_tokens = response.json()
            tokens["access_token"] = new_tokens["access_token"]
            if "refresh_token" in new_tokens:
                tokens["refresh_token"] = new_tokens["refresh_token"]
            tokens["expires_at"] = now + new_tokens.get("expires_in", 0)
            save_tokens(tokens)
            print("✅ 토큰 갱신 완료")
        else:
            print("❌ 토큰 갱신 실패:", response.text)
    else:
        print("✅ 기존 토큰 사용 가능")

    return tokens["access_token"]

# ✅ 카카오 메시지 전송
def send_kakao_message(text):
    access_token = get_valid_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": text,
            "link": {
                "web_url": "https://example.com"
            },
            "button_title": "확인"
        })
    }
    response = requests.post("https://kapi.kakao.com/v2/api/talk/memo/default/send", headers=headers, data=data)
    return response.json()

# ✅ POST 요청을 받아 메시지를 전송하는 웹훅 엔드포인트
@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    text = data.get("message", "📢 알림 도착!")  # JSON body에서 메시지를 추출
    result = send_kakao_message(text)
    return jsonify(result)

# ✅ 서버 상태 확인용 기본 페이지
@app.route("/")
def home():
    return "카카오톡 웹훅 서버 작동 중!"

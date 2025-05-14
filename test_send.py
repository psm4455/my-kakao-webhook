import requests
import json  # ← 중요!

# 발급받은 액세스 토큰
KAKAO_ACCESS_TOKEN = "yWrs880AkKfr7xohNWhRYE6nbIKhfbhXAAAAAQoXIiAAAAGWzyCIvBKZRqbpl2cW"

def send_kakao_message_to_me():
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {KAKAO_ACCESS_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    template = {
        "object_type": "text",
        "text": "📩 트레이딩뷰 신호가 도착했습니다!",
        "link": {
            "web_url": "https://www.tradingview.com",
            "mobile_web_url": "https://www.tradingview.com"
        },
        "button_title": "트레이딩뷰 보기"
    }

    data = {
        "template_object": json.dumps(template)  # ← 반드시 JSON 문자열로!
    }

    response = requests.post(url, headers=headers, data=data)

    print("응답 코드:", response.status_code)
    print("응답 내용:", response.json())

send_kakao_message_to_me()

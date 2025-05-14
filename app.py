from flask import Flask, request
import requests
import json

app = Flask(__name__)

KAKAO_ACCESS_TOKEN = "yWrs880AkKfr7xohNWhRYE6nbIKhfbhXAAAAAQoXIiAAAAGWzyCIvBKZRqbpl2cW"

def send_kakao_message(text):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {KAKAO_ACCESS_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    template = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://www.tradingview.com",
            "mobile_web_url": "https://www.tradingview.com"
        },
        "button_title": "트레이딩뷰 열기"
    }

    data = {
        "template_object": json.dumps(template)
    }

    response = requests.post(url, headers=headers, data=data)
    return response.status_code, response.json()

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.json
        alert_message = data.get("message", "📢 새로운 트레이딩뷰 신호가 도착했습니다!")
        status_code, response_data = send_kakao_message(alert_message)
        return {
            "result": "success",
            "kakao_response": response_data
        }, status_code
    except Exception as e:
        return {
            "result": "error",
            "message": str(e)
        }, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

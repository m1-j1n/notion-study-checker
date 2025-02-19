import os
import requests
from dotenv import load_dotenv

load_dotenv()

MATTERMOST_WEBHOOK_URL = os.getenv("MATTERMOST_WEBHOOK_URL")

def send_mattermost_message(message):
    """ Mattermost로 메시지 전송 """
    data = {"text": message}
    response = requests.post(MATTERMOST_WEBHOOK_URL, json=data)
    if response.status_code == 200:
        print("✅ Mattermost 메시지 전송 성공!")
    else:
        print(f"❌ 메시지 전송 실패: {response.status_code}, {response.text}")

# 🛠️ 단독 실행 시 테스트 가능하도록 수정
if __name__ == "__main__":
    send_mattermost_message("🚀 테스트 메시지: Mattermost 알림이 정상적으로 작동하는지 확인하세요!")
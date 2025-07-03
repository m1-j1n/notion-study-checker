import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def fetch_notion_data():
    """Notion API에서 현재 데이터베이스의 모든 페이지 가져오기"""
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"❌ Notion API 오류: {response.status_code}, {response.text}")
        return None
    
def get_missing_attendees_by_day():
    """오늘 날짜(YYYY-MM-DD)의 미참여자 정보 가져오기"""
    notion_data = fetch_notion_data()
    if not notion_data:
        return None

    kst = pytz.timezone("Asia/Seoul")
    today = datetime.now(kst).strftime("%Y-%m-%d")
    
    for item in notion_data.get("results", []):
        properties = item.get("properties", {})
        date_info = properties.get("진행일", {}).get("date", {}).get("start", "")

        if date_info[:10] == today:
            missing_attendees_prop = properties.get("미참여자", {}).get("multi_select", [])
            missing_attendees = [person["name"] for person in missing_attendees_prop]
            return date_info[:10], missing_attendees

    return None, []

# ✅ 직접 실행 시 테스트 코드
if __name__ == "__main__":
    date, missing_attendees = get_missing_attendees_by_day()
    if date:
        print(f"🔍 {date}의 미참여자 데이터: {missing_attendees}")
    else:
        print("금일 날짜에 해당하는 데이터가 없습니다.")

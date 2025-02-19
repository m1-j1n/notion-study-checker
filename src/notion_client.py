import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

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

def get_attendees_by_day():
    """오늘 날짜(YYYY-MM-DD)의 출석자 정보 가져오기"""
    notion_data = fetch_notion_data()
    if not notion_data:
        return {}

    today = datetime.today().strftime("%Y-%m-%d")  # 오늘 날짜 (예: '2025-02-19')
    today_attendees = {}

    print(f"✅ 오늘 날짜: {today}")  # 🔍 오늘 날짜 출력

    for item in notion_data.get("results", []):
        properties = item.get("properties", {})
        date_info = properties.get("진행일", {}).get("date", {}).get("start", None)
        attendees = properties.get("참여자", {}).get("multi_select", [])

        if date_info:
            date_info = date_info[:10]  # ✅ 'YYYY-MM-DD' 형식으로 변환

        # ✅ 필터링 전에 모든 데이터를 출력하는 것이 아니라, "오늘 날짜"만 출력하도록 변경!
        if date_info == today:
            attendees_list = [attendee["name"] for attendee in attendees]
            today_attendees[date_info] = attendees_list
            print(f"✅ 과제 여부 - 진행일: {date_info}, 출석자: {attendees_list}")  # ✅ 오늘 날짜만 출력

    return today_attendees

def create_study_page():
    """매주 월요일, 수요일 스터디 페이지 자동 생성"""
    today = datetime.today().strftime("%Y-%m-%d")
    day = datetime.today().strftime("%a")  # 'Mon' or 'Wed'
    korean_day_map = {"Mon": "월", "Wed": "수"}

    if day not in korean_day_map:
        return

    title = f"{korean_day_map[day]} : 스터디"

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "과목": {"title": [{"text": {"content": title}}]},
            "진행일": {"date": {"start": today}},
            "참여자": {"multi_select": []}
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(f"✅ {title} 페이지 생성 완료")
    else:
        print(f"❌ 페이지 생성 실패: {response.status_code}, {response.text}")

# ✅ 직접 실행 시 테스트 코드
if __name__ == "__main__":
    attendees = get_attendees_by_day()
    print("🔍 현재 요일의 출석 데이터:")
    print(json.dumps(attendees, indent=4, ensure_ascii=False))
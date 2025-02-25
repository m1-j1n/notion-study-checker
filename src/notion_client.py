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

    # 전체 데이터를 출력해서 확인
    print("🔍 Notion 원본 데이터 (처음 1개만 출력):")
    print(json.dumps(notion_data.get("results", [])[0], indent=4, ensure_ascii=False))

    today = datetime.today().strftime("%Y-%m-%d")  # 예: '2025-02-25'
    today_attendees = {}

    print(f"✅ 오늘 날짜: {today}")

    for index, item in enumerate(notion_data.get("results", [])):
        properties = item.get("properties", {})

        # 🚀 각 루프에서 현재 properties 상태 출력
        print(f"🔍 [{index}] 현재 properties 상태:")
        print(json.dumps(properties, indent=4, ensure_ascii=False))

        # 진행일 정보 가져오기
        date_info = None
        progress_prop = properties.get("진행일", {})

        if progress_prop is None:
            print(f"⚠️ [{index}] 진행일 프로퍼티 없음, None 처리됨")
        elif not isinstance(progress_prop, dict):
            print(f"⚠️ [{index}] 진행일 프로퍼티가 예상한 dict 타입이 아님: {progress_prop}")
        elif "date" not in progress_prop:
            print(f"⚠️ [{index}] 'date' 키 없음")
        elif progress_prop["date"] is None:
            print(f"⚠️ [{index}] 'date' 값이 None")
        else:
            date_info = progress_prop["date"].get("start")

        if date_info:
            date_info = date_info[:10]  # 'YYYY-MM-DD' 형식 변환
        else:
            print(f"⚠️ [{index}] 진행일 정보가 없음, 건너뜀")
            continue

        # 참여자 정보 가져오기
        attendees = properties.get("참여자", {}).get("multi_select", [])

        # 오늘 날짜와 일치하는 경우만 처리
        if date_info == today:
            attendees_list = [attendee["name"] for attendee in attendees]
            today_attendees[date_info] = attendees_list
            print(f"✅ [{index}] 과제 여부 - 진행일: {date_info}, 출석자: {attendees_list}")

    return today_attendees

# ✅ 직접 실행 시 테스트 코드
if __name__ == "__main__":
    attendees = get_attendees_by_day()
    print("🔍 현재 요일의 출석 데이터:")
    print(json.dumps(attendees, indent=4, ensure_ascii=False))

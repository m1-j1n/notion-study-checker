from notion_client import get_missing_attendees_by_day
from mattermost_client import send_mattermost_message
import schedule
import time

def check_and_notify():
    """ Notion DB에서 미참여자 정보를 가져와 Mattermost로 알림을 전송합니다. """
    date, missing_attendees = get_missing_attendees_by_day()

    if date is None:
        print("⚠️ 오늘 날짜에 해당하는 Notion 페이지가 없습니다.")
        return

    if missing_attendees:
        message = f"🚨 {date} 과제를 제출하지 않은 사람: {', '.join(missing_attendees)}"
    else:
        message = f"✅ {date} 모든 사람이 과제를 제출했습니다!"
    
    print(message)
    send_mattermost_message(message)

# 09:00에 출석 체크 후 알림 전송
schedule.every().monday.at("09:00").do(check_and_notify)
schedule.every().wednesday.at("09:00").do(check_and_notify)

if __name__ == "__main__":
    check_and_notify()

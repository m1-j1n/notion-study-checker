from notion_client import get_attendees_by_day
from mattermost_client import send_mattermost_message
import schedule
import time

EXPECTED_ATTENDEES = {"김미진", "박소현", "양재원", "정준웅", "조영우", "곽서현", "박민수", "이한민", "신범수"}

def check_and_notify():
    """ 출석 체크 후 미참여자 알림 전송 """
    attendees_dict = get_attendees_by_day()

    if not attendees_dict:
        print("⚠️ 오늘의 출석 페이지가 아직 생성되지 않음.")  # Mattermost 알림 없음
        return

    for date, attendees in attendees_dict.items():
        missing_attendees = EXPECTED_ATTENDEES - set(attendees)

        if missing_attendees:
            message = f"🚨 {date} 출석하지 않은 사람: {', '.join(missing_attendees)}"
            print(message)  # 콘솔 출력
            send_mattermost_message(message)  # Mattermost 알림 전송
        else:
            message = f"✅ {date} 모든 사람이 출석했습니다!"
            print(message)  # 콘솔 출력
            send_mattermost_message(message)  # Mattermost 알림 전송

# ✅ 09:00에 출석 체크 후 알림 전송
schedule.every().monday.at("09:00").do(check_and_notify)
schedule.every().wednesday.at("09:00").do(check_and_notify)

if __name__ == "__main__":
    check_and_notify()  # ✅ 한 번만 실행 후 종료
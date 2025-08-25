import requests
from datetime import datetime, timedelta
from config import SERVICE_KEY, NX, NY


# ----------
# 상수 정의
# ----------
CURRENT_YEAR = datetime.now().year
CURRENT_MONTH = datetime.now().month
CURRENT_DAY = datetime.now().day

CURRENT_HOUR = datetime.now().hour
CURRENT_MIN = datetime.now().minute


# ----------
# 함수 정의
# ----------
def format_hour(hour: int) -> str:
    """24시간 기준 시각을 오전/오후 문자열 변환"""

    period = "오전" if hour < 12 else "오후"
    hour12 = 12 if hour % 12 == 0 else hour % 12
    return f"{period} {hour12}시"


def print_weather(_data: dict, _display_hour: str):
    """주어진 시간과 데이터로 날씨 출력"""

    # 하늘 상태
    sky_dict = {'1': '맑음', '3': '구름많음', '4': '흐림'}
    sky = sky_dict.get(_data.get('SKY', '1'), '정보없음')

    # 기온
    tmp = _data.get('T1H', '0')

    # 습도
    reh = _data.get('REH', '0')

    # 강수 형태
    pty_dict = {
        '0': '없음', '1': '비', '2': '비/눈', '3': '눈',
        '4': '소나기', '5': '빗방울', '6': '빗방울 눈날림', '7': '눈날림'
    }
    pty = pty_dict.get(_data.get('PTY', '0'), '정보없음')

    # 강수량
    pcp = _data.get('RN1', '강수없음')

    # 강수 형태 따라 표시 다르게
    if pty == '없음':
        print(f"{_display_hour} : {sky} {tmp}'C (습도 {reh}%)")
    else:
        print(f"{_display_hour} : {sky} {tmp}'C (습도 {reh}%) / ({pty}, {pcp})")


def get_base_time() -> str:
    """45분이 넘으면 해당 시간, 아니면 직전 시간의 'HH30' 반환"""
    hour = CURRENT_HOUR if CURRENT_MIN > 45 else CURRENT_HOUR - 1
    return f"{hour:02d}30"


def get_base_date() -> str:
    """00:00~00:45 사이에는 전날 날짜 반환"""
    if CURRENT_HOUR == 0 and CURRENT_MIN < 45:
        # 하루 전으로 계산
        yesterday = datetime(CURRENT_YEAR, CURRENT_MONTH, CURRENT_DAY) - timedelta(days=1)
        return f"{yesterday.year}{yesterday.month:02d}{yesterday.day:02d}"

    return f"{CURRENT_YEAR}{CURRENT_MONTH:02d}{CURRENT_DAY:02d}"


# ----------
# 실행부
# ----------

base_time = get_base_time()
base_date = get_base_date()

# API URL 구성
url = (
    f"https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
    f"?serviceKey={SERVICE_KEY}"
    f"&pageNo=1&numOfRows=60&dataType=JSON"
    f"&base_date={base_date}&base_time={base_time}"
    f"&nx={NX}&ny={NY}"
)

# API 요청
response = requests.get(url)
data = response.json()
items = data['response']['body']['items']['item']

# 시간별 데이터 담을 딕셔너리 생성
weather_by_time = {}

# 각 항목을 시간 별로 정리
for item in items:
    time = item['fcstTime']
    category = item['category']
    value = item['fcstValue']

    if time not in weather_by_time:
        weather_by_time[time] = {}

    weather_by_time[time][category] = value

# 각 시간에 대해 출력 (현재 시간, 앞으로 3시간의 예보)
print(f"< {CURRENT_YEAR}년 {CURRENT_MONTH}월 {CURRENT_DAY}일 날씨 예보 >")
print("# 현재 날씨입니다.\n")

for i in range(1, 5):
    now = f"{(CURRENT_HOUR + i) % 24:02d}00"
    data = weather_by_time[now]
    display_hour = format_hour(CURRENT_HOUR + i - 1)
    print_weather(data, display_hour)

    if i == 1:
        print()
        print("-" * 40)
        print()
        print("# 앞으로 3시간의 날씨 예보입니다.\n")

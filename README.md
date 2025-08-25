# 📌 초단기 날씨 예보 조회 프로그램 (Python)

## 🔹 프로젝트 개요

이 프로그램은 한국 기상청의 초단기 예보 API를 활용하여,

입력한 사용자의 위치 기준으로 현재 날씨와 앞으로 3시간의 날씨 예보를 출력합니다.

<br>

파이썬 requests 라이브러리를 사용하여 데이터를 가져오며,
콘솔에서 확인할 수 있습니다.

맥의 경우 Automator 를 사용해
Dock 에 아이콘으로 바로 실행할 수 있습니다.

<br>

(작업 내용 Velog : [여기로!]())

<br>

## 🔹 주요 기능

- 현재 시각 및 이후 시간의 날씨 예보 조회
- 시간대별 온도, 습도, 하늘 상태, 강수 형태, 강수량 출력
- 오전/오후 시각 변환 표시

<br>

## 🔹 사용 방법
1. 저장소 클론
```
git clone https://github.com/iaminwoo/weather_fetch.git
```

2. 의존성 설치
```
pip install requests
```

3. 기상청 API 신청 및 키 발급, 좌표 확인

[https://www.data.go.kr/data/15084084/openapi.do](https://www.data.go.kr/data/15084084/openapi.do)

4. config_template.py 를 복사해 config.py 파일 작성
```
SERVICE_KEY = "발급받은_기상청_API_KEY"
NX = "원하는_지역의_x좌표"
NY = "원하는_지역의_y좌표"
```

5. 스크립트 실행
```
python weather_fetch.py
```

<br>

## 🔹 코드 구조

- weather_fetch.py : 메인 실행 파일
- config.py : API 키 및 위치 좌표 저장

### 함수 설명:
- format_hour(hour) : 24시간 기준을 오전/오후 문자열로 변환
- print_weather(_data, _display_hour) : 시간별 날씨 데이터 출력
- get_base_time() : API 요청용 기준 시각 계산
- get_base_date() : API 요청용 기준 날짜 계산

<br>

## 🔹 예시 출력

```
< 2025년 8월 25일 날씨 예보 >
# 현재 날씨입니다.

오후 3시 : 흐림 32'C (습도 60%) / (비, 1mm 미만)

----------------------------------------

# 앞으로 3시간의 날씨 예보입니다.

오후 4시 : 구름많음 31'C (습도 65%)
오후 5시 : 맑음 30'C (습도 75%)
오후 6시 : 구름많음 27'C (습도 75%)
```

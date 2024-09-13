import requests
import icalendar
import datetime
from bs4 import BeautifulSoup

# 気象庁の津軽の週間天気予報URL
WEATHER_URL = "https://www.jma.go.jp/bosai/forecast/data/overview_week/020000.json"

# 取得したデータをiCal形式に変換して出力
def create_ical(weather_data):
    cal = icalendar.Calendar()
    cal.add('prodid', '-//Tsugaru Weather//example.com//')
    cal.add('version', '2.0')

    # 現在の日付を取得
    today = datetime.date.today()

    # 週間天気予報のデータを元にiCalイベントを作成
    for i, forecast in enumerate(weather_data['text'].split("　")):
        event = icalendar.Event()
        event.add('summary', f"津軽の天気予報: {forecast}")
        event.add('dtstart', today + datetime.timedelta(days=i))
        event.add('dtend', today + datetime.timedelta(days=i+1))
        cal.add_component(event)

    # iCalファイルを保存
    with open("tsugaru_weather.ics", "wb") as f:
        f.write(cal.to_ical())

# 天気データの取得
def fetch_weather():
    response = requests.get(WEATHER_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data: {response.status_code}")
        return None

def main():
    weather_data = fetch_weather()
    if weather_data:
        create_ical(weather_data)
        print("iCal file created: tsugaru_weather.ics")

if __name__ == "__main__":
    main()

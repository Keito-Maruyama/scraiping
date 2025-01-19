import requests
from bs4 import BeautifulSoup
import csv

def fetch_html(url):
  try:
    response = requests.get(url)
    response.raise_for_status()  # エラー発生時に例外を発生させる
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"Failed to fetch HTML: {e}")
    return None

def parse_html(html):
  return BeautifulSoup(html, 'html.parser')

def extract_period_details(period_data):
  # period_data から曜日と時限を抽出する処理
  # 例: "Period月曜1限" -> ["月", 1]
  # 曜日は月曜〜金曜を1〜5で表す。時限はそのまま数値として扱う。
  # 適切な正規表現などを用いて抽出する

  # 以下はサンプル実装です。実際のデータに合わせて修正してください。
  try:
    day_str = period_data.split('Period')[1].split('限')[0]  # "月曜1" のような文字列を取得
    day = ['月', '火', '水', '木', '金'].index(day_str[0]) + 1  # 曜日を数値に変換
    time = int(day_str[1:])  # 時限を数値に変換
    return [day, time]
  except:
    return [None, None]  # 曜日と時限が取得できない場合は None を返す

def extract_data(soup):
  # 早稲田大学の講義カタログページから必要なデータを抽出する処理
  period_data = soup.select_one('table.detail tr:nth-of-type(1) td').text.strip()
  period_day, period_time = extract_period_details(period_data)

  data = {
    'id': "-",  # UUID はここでは生成できないので、"-" で代用
    'course_name': soup.select_one('h2.detail-title span').text.strip(),
    'course_code': soup.select_one('span.detail-course-code').text.strip(),
    'department_id': "-",  # 所属学部・学科の ID は取得できないので、"-" で代用
    'semester': soup.select_one('table.detail tr:nth-of-type(2) td').text.strip(),
    'genre': "-",  # 授業ジャンルの情報は取得できないので、"-" で代用
    'description': soup.select_one('div.detail-text.white-space-pre-wrap').text.strip(),
    'objectives': "-",  # 授業目標の情報は取得できないので、"-" で代用
    'content': "-",  # 授業内容の情報は取得できないので、"-" で代用
    'instructor_id': "-",  # 教授の ID は取得できないので、"-" で代用
    'grading_criteria': "-",  # 成績評価基準の情報は取得できないので、"-" で代用
    'examination_format': "-",  # 試験形式の情報は取得できないので、"-" で代用
    'teaching_method': soup.select_one('table.detail tr:nth-of-type(1) td').text.strip(),
    'class_days': period_day,
    'class_period': period_time,
    'class_location': soup.select_one('table.detail tr:nth-of-type(3) td').text.strip(),
    'attendance_policy': "-",  # 出席要件の情報は取得できないので、"-" で代用
    'target_students': "-",  # 対象学生の情報は取得できないので、"-" で代用
    'capacity': "-",  # 定員人数の情報は取得できないので、"-" で代用
    'university_id': "-",  # 大学 ID は取得できないので、"-" で代用
    'accredited_universities': "-",  # 単位が認められる他の大学の一覧は取得できないので、"-" で代用
    'additional_info': "-",  # 補足情報は取得できないので、"-" で代用
    'created_at': "-",  # 作成日時は取得できないので、"-" で代用
    'updated_at': "-"  # 最終更新日時は取得できないので、"-" で代用
  }
  return data

def save_to_csv(data, filename="database_test.csv"):
  with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data.values())

for i in range(3):
  id = i + 40001
  url = f"http://catalog.he.u-tokyo.ac.jp/jd-detail?code={id}&year=2018"
  
  html = fetch_html(url)
  if html:
    soup = parse_html(html)
    data = extract_data(soup)
    save_to_csv(data)
    
    time.sleep(0.4)  # サーバー負荷軽減のためのインターバル
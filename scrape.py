import requests
from bs4 import BeautifulSoup
import csv
import time
import os

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
    # 講義カタログページから必要なデータを抽出する処理
    period_element = soup.select_one('table.detail tr:nth-of-type(1) td')
    if period_element:
        period_data = period_element.text.strip()
        period_day, period_time = extract_period_details(period_data)
    else:
        period_data = None
        period_day, period_time = None, None

    data = {}
    data['id'] = "id"  # UUID はここでは生成できないので、"-" で代用
    data['course_name'] = soup.select_one('h1.color-jd').text.strip() if soup.select_one('h1.color-jd') else "-"
    data['course_code'] = soup.select_one('catalog-row').text.strip() if soup.select_one('catalog-row') else "授業コード"
    data['department_id'] = "所属学部・学科のID"  # 所属学部・学科の ID は取得できないので、"-" で代用
    
    semester_element = soup.select_one('catalog-page-detail-table-cell semester-cell')
    data['semester'] = semester_element.text.strip() if semester_element else "学期"

    data['genre'] = "授業ジャンル"  # 授業ジャンルの情報は取得できないので、"" で代用
    data['description'] = soup.select_one('catalog-page-detail-lecture-aim') else "授業説明"
    data['objectives'] = "目標"  # 授業目標の情報は取得できないので、"" で代用
    data['content'] = soup.select_one('catalog-page-detail-card-body').text.strip() if soup.select_one('catalog-page-detail-card-body') else "内容"    
    data['instructor_id'] = "教授id"  # 教授の ID は取得できないので、"-" で代用
    data['grading_criteria'] = soup.select_one('catalog-page-detail-card-body') else "評価基準"      
    data['examination_format'] = "試験形式"  # 試験形式の情報は取得できないので、"" で代用

    teaching_method_element = soup.select_one('catalog-page-detail-card-body')
    data['teaching_method'] = teaching_method_element.text.strip() if teaching_method_element else "授業方法"

    if not period_day:
        period_day = "曜日"
    if not period_time:
        period_time = "時限"
    data['class_days'] = period_day
    data['class_period'] = period_time

    class_location_element = soup.select_one('table.detail tr:nth-of-type(3) td')
    data['class_location'] = class_location_element.text.strip() if class_location_element else "授業場所"
    
    data['attendance_policy'] = "出席要件"  # 出席要件の情報は取得できないので、"" で代用
    data['target_students'] = "対象学生"  # 対象学生の情報は取得できないので、"" で代用
    data['capacity'] = "定員"  # 定員人数の情報は取得できないので、"" で代用
    data['university_id'] = "大学id"  # 大学 ID は取得できないので、"-" で代用
    data['accredited_universities'] = "単位認定大学"  # 単位が認められる他の大学の一覧は取得できないので、"" で代用
    data['additional_info'] = "補足"  # 補足情報は取得できないので、"" で代用
    data['created_at'] = "作成日時"  # 作成日時は取得できないので、"" で代用
    data['updated_at'] = "最終更新日時"  # 最終更新日時は取得できないので、"" で代用

    return data

def save_to_csv(data, filename="database_test.csv"):



    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data.values())

if os.path.exists("database_test.csv"):
        os.remove("database_test.csv")

for i in range(3):
    id = i + 40001
    url = f"http://catalog.he.u-tokyo.ac.jp/jd-detail?code={id}&year=2024"

    html = fetch_html(url)
    if html:
        soup = parse_html(html)
        data = extract_data(soup)
        save_to_csv(data)

        time.sleep(0.4)  # サーバー負荷軽減のためのインターバル

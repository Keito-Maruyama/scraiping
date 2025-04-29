import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime 
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
    # 例: "月曜2限" -> ["月曜", "2限"]
    try:
        day = period_data[:-2]  # 最後の2文字（"限"）を削除
        time = period_data[-2:]  # 最後の2文字（"限"を含む）を抽出
        return [day, time]
    except:
        return [None, None]  # 曜日と時限が取得できない場合は None を返す


def extract_data(soup):
    # 講義カタログページから必要なデータを抽出する処理
 
    data = {}
    data['id'] = "id"  # UUID はここでは生成できないので、"-" で代用
    data['course_name'] = soup.select_one('h1.color-jd').text.strip() if soup.select_one('h1.color-jd') else "-"
    
    course_code_element = soup.select_one('#catalog-main-container > div.catalog-page-detail-scrollable-container.catalog-horizontal-scrollable-container > div > div > div.catalog-page-detail-table-row.catalog-table-row-in-mylist-2024-40001 > div.catalog-row > div.catalog-page-detail-table-cell.code-cell')
    data['course_code'] = course_code_element.text.strip() if soup.select_one('#catalog-main-container > div.catalog-page-detail-scrollable-container.catalog-horizontal-scrollable-container > div > div > div.catalog-page-detail-table-row.catalog-table-row-in-mylist-2024-40001 > div.catalog-row > div.catalog-page-detail-table-cell.code-cell') else "授業コード"
    
    data['department_id'] = "所属学部・学科のID"  # 所属学部・学科の ID は取得できないので、"-" で代用
    
    semester_element = soup.select_one('.semester-cell span')
    data['semester'] = semester_element.text.strip() if soup.select_one('.semester-cell span') else "学期"

    data['genre'] = "授業ジャンル"  # 授業ジャンルの情報は取得できないので、"" で代用
   
    description_element = soup.select_one('#catalog-main-container > div.catalog-page-common-container > div.catalog-page-detail-lecture-aim')
    data['description'] = description_element.text.strip() if description_element else "授業説明"
    
    data['objectives'] = "目標"  # 授業目標の情報は取得できないので、"" で代用
    
    content_element = soup.select_one('#catalog-main-container > div.catalog-page-detail-card-container > div > div:nth-child(1) > div.catalog-page-detail-card-body > div')
    data['content'] = content_element.text.strip() if soup.select_one('#catalog-main-container > div.catalog-page-detail-card-container > div > div:nth-child(1) > div.catalog-page-detail-card-body > div') else "内容"    
    
    data['instructor_id'] = "教授id"  # 教授の ID は取得できないので、"-" で代用
    
    grading_criteria_element = soup.select_one('#catalog-main-container > div.catalog-page-detail-card-container > div > div:nth-child(3) > div.catalog-page-detail-card-body > div')
    data['grading_criteria'] = grading_criteria_element.text.strip() if soup.select_one('#catalog-main-container > div.catalog-page-detail-card-container > div > div:nth-child(3) > div.catalog-page-detail-card-body > div') else "評価基準"      
    
    data['examination_format'] = "試験形式"  # 試験形式の情報は取得できないので、"" で代用

    teaching_method_element = soup.select_one('#catalog-main-container > div.catalog-page-detail-card-container > div > div:nth-child(2) > div.catalog-page-detail-card-body > div')
    data['teaching_method'] = teaching_method_element.text.strip() if teaching_method_element else "授業方法"


    period_element = soup.select_one('div.catalog_row:nth-of-type(1)> div:nth-child(5)')
    if period_element:
       period_data = period_element[0].text.strip()  # リストの最初の要素にアクセス
       period_day, period_time = extract_period_details(period_data)
    else:
     period_day = "曜日"
     period_time = "時限" 
     data['class_days'] = period_element
     data['class_period'] = period_time


    class_location_element = soup.select_one('table.detail tr:nth-of-type(3) td')
    data['class_location'] = class_location_element.text.strip() if class_location_element else "授業場所"
    
    data['attendance_policy'] = "出席要件"  # 出席要件の情報は取得できないので、"" で代用
    data['target_students'] = "対象学生"  # 対象学生の情報は取得できないので、"" で代用
    data['capacity'] = "定員"  # 定員人数の情報は取得できないので、"" で代用
    data['university'] = "大学名"  
    data['accredited_universities'] = "単位認定大学"  # 単位が認められる他の大学の一覧は取得できないので、"" で代用
    data['additional_info'] = "補足"  # 補足情報は取得できないので、"" で代用
    data['created_at'] = "作成日時"  # 作成日時は取得できないので、"" で代用
    now = datetime.now()
    data['updated_at'] = now.strftime('%Y-%m-%d %H:%M:%S')

    return data

def save_to_csv(data, filename="database_test.csv"):

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([[value] for value in data.values()])  

if os.path.exists("database_test.csv"):
        os.remove("database_test.csv")
        with open("database_test.csv", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            header = ["一意のコース識別子", "授業名", "授業コード", "所属学部・学科(Department テーブルへの外部キー)", "開講学期", "授業ジャンル(例：文系、理系、専門分野など)", "授業概要", "授業目標", "授業内容", "教授の識別子(Instructor テーブルへの外部キー)", "成績評価基準", "試験形式 (詳細)", "授業形式", "授業曜日", "授業時限", "授業場所", "出席要件", "対象学生", "定員人数", "大学ID(University テーブルへの外部キー)", "単位が認められる他の大学の一覧", "補足情報", "作成日時", "最終更新日時"]
            writer.writerow(header)

for i in range(3):
    id = i + 40001
    url = f"http://catalog.he.u-tokyo.ac.jp/jd-detail?code={id}&year=2024"

    html = fetch_html(url)
    if html:
        soup = parse_html(html)
        data = extract_data(soup)
        save_to_csv(data)

        time.sleep(0.4)  # サーバー負荷軽減のためのインターバル

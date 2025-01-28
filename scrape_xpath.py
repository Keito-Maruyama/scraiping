import requests
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime 
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
    # 例: "月曜2限" -> ["月曜", "2限"]
    try:
        day = period_data[:-2]  # 最後の2文字（"限"）を削除
        time = period_data[-2:]  # 最後の2文字（"限"を含む）を抽出
        return [day, time]
    except:
        return [None, None]  # 曜日と時限が取得できない場合は None を返す


def extract_data(soup):
     
    tree = etree.HTML(str(soup))

    # 講義カタログページから必要なデータを抽出する処理
    period_element = tree.xpath('//*[@id="catalog-main-container"]/div[5]/div/div/div[2]/div[1]/div[5]')
    if period_element:
        period_data = period_element[0].text.strip()  # リストの最初の要素にアクセス
        period_day, period_time = extract_period_details(period_data)
    else:
        period_data = None
        period_day, period_time = None, None

   
    data = {}

    data['id'] = "id"  # id はここでは生成できないので
   
    data['course_name'] = soup.select_one('h1.color-jd').text.strip() if soup.select_one('h1.color-jd') else "-"
    
    #course_code
    course_code_element=tree.xpath('//*[@id="catalog-main-container"]/div[5]/div/div/div[2]/div[1]/div[1]/div[2]')
    if course_code_element: data['course_code'] = course_code_element[0].text.strip() 
    else: data['course_code']="授業コード"

    # department_id 取得不可能
    data['department_id'] = "所属学部・学科ID"

    # semester
    semester_element = tree.xpath('//*[@id="catalog-main-container"]/div[5]/div/div/div[2]/div[1]/div[4]/span')
    if semester_element:data['semester'] = semester_element[0].text.strip()
    else:data['semester'] = "学期"

    # genre 記載なし
    data['genre'] = "授業ジャンル"

    # description　
    description_element = tree.xpath('//*[@id="catalog-main-container"]/div[5]/div/div/div[2]/div[1]/div[4]')
    if description_element:data['description'] = description_element[0].text.strip()
    else:data['description'] = "講義の説明"

    # objectives　記載なし
    data['objectives'] = "授業目標"

    # content
    content_element = tree.xpath('//*[@id="catalog-main-container"]/div[6]/div/div[1]/div[2]/div')
    if content_element:data['content'] = content_element[0].text.strip()
    else:data['content'] = "授業内容"

    # instructor_id　取得不可能
    data['instructor_id'] = "教授のID"

    # grading_criteria
    grading_criteria_element = tree.xpath('//*[@id="catalog-main-container"]/div[6]/div/div[3]/div[2]/div')
    if grading_criteria_element:data['grading_criteria'] = grading_criteria_element[0].text.strip()
    else:data['grading_criteria'] = "成績評価基準"

    # examination_format 記載なし
    data['examination_format'] = "試験形式"

    # teaching_method
    teaching_method_element = tree.xpath('//*[@id="catalog-main-container"]/div[6]/div/div[2]/div[2]/div')
    if teaching_method_element:data['teaching_method'] = teaching_method_element[0].text.strip()
    else:data['teaching_method'] = "授業形式"
    

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


for i in range(10):
    id = i + 40001
    url = f"http://catalog.he.u-tokyo.ac.jp/jd-detail?code={id}&year=2024"
    html = fetch_html(url)
    if html:
        soup = parse_html(html)
        data = extract_data(soup)
        save_to_csv(data)
        time.sleep(0.4)  # サーバー負荷軽減のためのインターバル

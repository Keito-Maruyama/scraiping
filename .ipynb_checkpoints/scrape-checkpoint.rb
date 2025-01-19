
require 'open-uri'
require 'nokogiri'
require 'csv'

def fetch_html(url)
  URI.open(url).read
rescue StandardError => e
  puts "Failed to fetch HTML: #{e.message}"
  nil
end

def parse_html(html, charset)
  Nokogiri::HTML.parse(html, nil, charset)
end

def extract_data(contents)# 大学の講義カタログページから必要なデータを抽出する処理
  period_data = contents.at('//table[@class="detail"]/tr[1]/td').text.strip
  period_day, period_time = extract_period_details(period_data) 

  {
    id: "-", # UUID はここでは生成できないので、"-" で代用
    course_name: contents.at('//h2[@class="detail-title"]/span').text.strip,
    course_code: contents.at('//span[@class="detail-course-code"]').text.strip,
    department_id: "-", # 所属学部・学科の ID は取得できないので、"-" で代用
    semester: contents.at('//table[@class="detail"]/tr[2]/td').text.strip,
    genre: "-", # 授業ジャンルの情報は取得できないので、"-" で代用
    description: contents.at('//div[@class="detail-text white-space-pre-wrap"]').text.strip,
    objectives: "-", # 授業目標の情報は取得できないので、"-" で代用
    content: "-", # 授業内容の情報は取得できないので、"-" で代用
    instructor_id: "-", # 教授の ID は取得できないので、"-" で代用
    grading_criteria: "-", # 成績評価基準の情報は取得できないので、"-" で代用
    examination_format: "-", # 試験形式の情報は取得できないので、"-" で代用
    teaching_method: contents.at('//table[@class="detail"]/tr[1]/td').text.strip,
    class_days: period_day,
    class_period: period_time,
    class_location: contents.at('//table[@class="detail"]/tr[3]/td').text.strip,
    attendance_policy: "-", # 出席要件の情報は取得できないので、"-" で代用
    target_students: "-", # 対象学生の情報は取得できないので、"-" で代用
    capacity: "-", # 定員人数の情報は取得できないので、"-" で代用
    university_id: "-", # 大学 ID は取得できないので、"-" で代用
    accredited_universities: "-", # 単位が認められる他の大学の一覧は取得できないので、"-" で代用
    additional_info: "-", # 補足情報は取得できないので、"-" で代用
    created_at: "-", # 作成日時は取得できないので、"-" で代用
    updated_at: "-" # 最終更新日時は取得できないので、"-" で代用
  }
end

def extract_period_details(period_data)# period_data から曜日と時限を抽出する処理
  # 例: "Period月曜1限" -> ["月", 1]
  # 曜日は月曜〜金曜を1〜5で表す。時限はそのまま数値として扱う。
  # 適切な正規表現などを用いて抽出する
  match_data = period_data.match(/Period(.*?)([1-6])限/)
  if match_data
    day_str = match_data[1]
    time = match_data[2].to_i
    day = case day_str
          when "月曜" then 1
          when "火曜" then 2
          when "水曜" then 3
          when "木曜" then 4
          when "金曜" then 5
          else nil # 曜日が取得できない場合は nil を返す
          end
    return [day, time]
  else
    return [nil, nil] # 曜日と時限が取得できない場合は nil を返す
  end
end


def save_to_csv(data, filename = "database_test.csv")
  CSV.open(filename, "a+") do |csv|
    csv << data.values
  end
end

3.times do |i|
  id = i + 40001
  url = "http://catalog.he.u-tokyo.ac.jp/jd-detail?code=#{id}&year=2018" # 東京大学のURL
  
  html = fetch_html(url)
  next unless html
  
  contents = parse_html(html, 'utf-8')
  data = extract_data(contents)
  
  save_to_csv(data)
  
  sleep(0.4) # サーバー負荷軽減のためのインターバル
end
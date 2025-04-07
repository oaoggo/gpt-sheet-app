from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# 🔐 Render 환경에서만 작동 (로컬에서는 실행 안 됨)
if os.environ.get("CREDENTIAL_JSON") and not os.path.exists("credentials.json"):
    with open("credentials.json", "w") as f:
        f.write(os.environ.get("CREDENTIAL_JSON"))

# 🔑 Google Sheets 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 📄 시트 접근
spreadsheet = client.open_by_key("1AL4zGOjd5wXpEhxq3OZupMS-NM5oDUrqDfibV9GHZwU")
sheet = spreadsheet.get_worksheet_by_id(1128512406)

@app.route('/', methods=['GET'])
def home():
    return "🟢 GPTs 액션 서버가 실행 중입니다."

@app.route('/query', methods=['POST'])
def query():
    try:
        data = sheet.get_all_records()
        question = request.json.get("question", "")

        return jsonify({
            "question": question,
            "sheet_data": data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

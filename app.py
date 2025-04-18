import json
from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from flask import send_from_directory

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

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.well-known', 'ai-plugin.json', mimetype='application/json')

@app.route('/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='application/yaml')

@app.route('/logo.png')
def serve_logo():
    return send_from_directory('.', 'logo.png', mimetype='image/png')


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

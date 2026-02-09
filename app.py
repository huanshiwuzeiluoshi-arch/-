import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# --- 設定（.envから読み込み） ---
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

DEEPL_URL = "https://api-free.deepl.com/v2/translate" 

@app.route('/')
def form():
    # 起動時の読み込み画面
    return render_template('load.html')

@app.route('/daily-report')
def daily_report():
    # 日報などの個別ページ
    return render_template('page.html')

@app.route("/index", methods=["GET", "POST"])
def index():
    translated = ""
    original = ""

    if request.method == "POST":
        original = request.form.get("text", "")
        target_lang = request.form.get("target", "EN")

        if not original:
            return render_template("index.html", original="", translated="テキストを入力してください。")

        # DeepL APIへのリクエスト（ヘッダー認証方式）
        headers = {
            "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
        }
        data = {
            "text": original,
            "target_lang": target_lang
        }

        try:
            # APIリクエスト実行
            res = requests.post(DEEPL_URL, headers=headers, data=data)
            
            res.raise_for_status()
            
            # JSONを解析
            result = res.json()
            translated = result["translations"][0]["text"]

        except requests.exceptions.HTTPError as http_err:
            
            print(f"HTTP error occurred: {http_err}")
            translated = f"APIエラー（{res.status_code}）: キーやURLが間違ってるお。"
        except Exception as e:
            print(f"Other error occurred: {e}")
            translated = f"予期せぬエラーが発生したお: {str(e)}"

    return render_template("index.html", original=original, translated=translated)

if __name__ == "__main__":
    # サーバーが指定するポート番号を取得（なければ5000）
    # ※ファイルの先頭に「import os」があることを確認してください
    port = int(os.environ.get("PORT", 5000))
    
    # 外部公開用の設定（debugはFalseにするのが安全です）
    app.run(host="0.0.0.0", port=port, debug=False)
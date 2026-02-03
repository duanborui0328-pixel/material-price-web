from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

def mock_data(keyword):
    return [
        {
            "input_desc": keyword,
            "lang": "中文" if any("\u4e00" <= c <= "\u9fff" for c in keyword) else "英文",
            "platform": "Shopee",
            "title": f"{keyword} Sample Product A",
            "image": "https://via.placeholder.com/80",
            "price_idr": 12500
        },
        {
            "input_desc": keyword,
            "lang": "英文",
            "platform": "TikTok Shop",
            "title": f"{keyword} Sample Product B",
            "image": "https://via.placeholder.com/80",
            "price_idr": 13900
        }
    ]

@app.route("/", methods=["GET", "POST"])
def index():
    data = []
    keyword = ""

    if request.method == "POST":
        keyword = request.form.get("keyword", "")
        data = mock_data(keyword)

        df = pd.DataFrame(data)
        os.makedirs("output", exist_ok=True)
        df.to_excel("output/results.xlsx", index=False)

    return render_template("index.html", data=data, keyword=keyword)

@app.route("/download")
def download():
    return send_file("output/results.xlsx", as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

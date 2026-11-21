from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Cloud PaaS Lab 3</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #e3f2fd, #f5f7fa);
                margin: 0;
                text-align: center;
            }
            .container {
                margin: 100px auto;
                background: white;
                padding: 40px;
                width: 70%;
                max-width: 700px;
                border-radius: 20px;
                box-shadow: 0 5px 20px #cccccc;
            }
            h1 { color: #1565c0; }
            .success {
                color: green;
                font-weight: bold;
            }
            button {
                background: #1565c0;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 8px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Ứng dụng Cloud PaaS</h1>
            <h2>Bài thực hành 3 - Điện toán đám mây</h2>
            <p class="success">Ứng dụng Flask đã triển khai thành công!</p>
            <p>Nền tảng triển khai: Render Cloud Platform</p>
            <p>Framework: Python Flask</p>
            <p>Ứng dụng web đang hoạt động trên môi trường Cloud.</p>
            <button onclick="alert('Ứng dụng hoạt động bình thường!')">
                Kiểm tra ứng dụng
            </button>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

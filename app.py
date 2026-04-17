from app import create_app

app = create_app()

if __name__ == '__main__':
    # 啟動 Flask 開發伺服器
    app.run(debug=True, port=5000)

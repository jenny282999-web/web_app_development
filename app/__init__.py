import os
import sqlite3
from flask import Flask

def create_app(test_config=None):
    # 建立與設定 app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    
    if test_config is not None:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在，這樣 SQLite 才有地方寫入
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # 初始化資料庫邏輯（若資料庫不存在則讀取 schema.sql）
    def init_db():
        db_path = os.path.join(app.instance_path, 'database.db')
        schema_path = os.path.join(os.path.dirname(app.root_path), 'database', 'schema.sql')
        if not os.path.exists(db_path) and os.path.exists(schema_path):
            conn = sqlite3.connect(db_path)
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
            conn.close()
            print("資料庫初始化完成！")

    with app.app_context():
        init_db()
        
    # 載入並註冊剛才建立的 Blueprint 路由
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.divination_routes import divination_bp
    from app.routes.profile_routes import profile_bp
    from app.routes.donation_routes import donation_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(divination_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(donation_bp)
    
    return app

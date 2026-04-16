from flask import Flask

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.fortune import fortune_bp
    from app.routes.payment import payment_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(fortune_bp)
    app.register_blueprint(payment_bp)
    
    return app

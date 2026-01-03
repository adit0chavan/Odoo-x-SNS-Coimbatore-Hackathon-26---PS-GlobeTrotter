from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    from app.routes import auth, trips, activities, admin, profile, api as api_routes, community
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(trips.bp)
    app.register_blueprint(activities.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(api_routes.bp)
    app.register_blueprint(community.bp)
    
    with app.app_context():
        db.create_all()
    
    return app

from app import models

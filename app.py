from flask import Flask
from services.routes import auth, config, main
from services.sqlalchemy import init_db
from services.login_manager import init_login_manager

if __name__ == '__main__':
    app = Flask(__name__)
    
    # Flask Configuration
    app.config['SECRET_KEY'] = "SUP3R__S3CR3T__K3Y"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mariadb+mariadbconnector://admin:Password!123@127.0.0.1:3306/sgaa" #Mudar de acordo com sua configuração da database

    # Database Configuration
    init_db(app)

    # Initialize LoginManager
    init_login_manager(app)

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(config, url_prefix='/config')
    app.register_blueprint(main, url_prefix='/')

    app.run(port=80)
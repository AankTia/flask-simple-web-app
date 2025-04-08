from flask import Flask
from database import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '10c0a5fff9be4446b729f71d8543ca36'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprint
    from routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
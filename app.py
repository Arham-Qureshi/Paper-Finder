from models import db
from flask import Flask, render_template

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions here
    from models import db
    db.init_app(app)

    # Register blueprints here
    from routes import main as main_bp
    app.register_blueprint(main_bp)



    return app

if __name__ == '__main__':
    from models import db
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)

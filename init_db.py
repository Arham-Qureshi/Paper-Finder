from app import create_app
from models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully at " + app.config['SQLALCHEMY_DATABASE_URI'])

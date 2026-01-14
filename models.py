from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paper(db.Model):
    id = db.Column(db.String(100), primary_key=True) # arXiv ID
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.String(500))
    published_date = db.Column(db.Date)
    summary = db.Column(db.Text) # Abstract
    pdf_link = db.Column(db.String(255))
    doi = db.Column(db.String(100))
    citation_count = db.Column(db.Integer, default=0)
    ai_summary_short = db.Column(db.Text)
    ai_summary_bullets = db.Column(db.Text)

    def __repr__(self):
        return f'<Paper {self.title}>'

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.String(100), db.ForeignKey('paper.id'), nullable=False)
    user_notes = db.Column(db.Text)
    tags = db.Column(db.String(200)) # Comma separated tags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    paper = db.relationship('Paper', backref=db.backref('bookmarks', lazy=True))

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.Text, nullable=False) # Store as JSON string or plain text
    search_queries = db.Column(db.Text, nullable=False) # e.g. "CAD AutoCAD", "GIS ArcGIS"

    jobs = db.relationship('Job', backref='candidate', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'skills': self.skills,
            'search_queries': self.search_queries
        }

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    url = db.Column(db.String(500), unique=True, nullable=False)
    source = db.Column(db.String(50), default='LinkedIn')
    match_score = db.Column(db.Integer, default=0)
    posted_date = db.Column(db.String(100)) # e.g. "1 day ago"
    is_us_citizen_required = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='New') # New, Applied, Dismissed
    search_keyword = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'url': self.url,
            'source': self.source,
            'search_keyword': self.search_keyword,
            'match_score': self.match_score,
            'posted_date': self.posted_date,
            'status': self.status,
            'is_us_citizen_required': self.is_us_citizen_required,
            'created_at': self.created_at.isoformat()
        }

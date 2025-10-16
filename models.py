from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def utcnow():
    """Return current UTC time with timezone"""
    return datetime.now(timezone.utc)

class Transcript(db.Model):
    """Model for storing sales call transcripts"""
    __tablename__ = 'transcripts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    call_date = db.Column(db.DateTime, nullable=False, default=utcnow)
    client_name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    processed = db.Column(db.Boolean, default=False)
    
    # Relationship to insights
    insights = db.relationship('Insight', backref='transcript', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'call_date': self.call_date.isoformat() if self.call_date else None,
            'client_name': self.client_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed': self.processed,
            'insights': [insight.to_dict() for insight in self.insights]
        }


class Insight(db.Model):
    """Model for storing extracted product insights"""
    __tablename__ = 'insights'
    
    id = db.Column(db.Integer, primary_key=True)
    transcript_id = db.Column(db.Integer, db.ForeignKey('transcripts.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # e.g., 'feature_request', 'pain_point', 'positive_feedback'
    content = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(50))  # e.g., 'positive', 'negative', 'neutral'
    priority = db.Column(db.String(50))  # e.g., 'high', 'medium', 'low'
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'transcript_id': self.transcript_id,
            'category': self.category,
            'content': self.content,
            'sentiment': self.sentiment,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

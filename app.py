from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, timezone
from config import Config
from models import db, Transcript, Insight
from openai_service import OpenAIService
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)

# Initialize OpenAI service
openai_service = OpenAIService()


@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')


@app.route('/api/transcripts', methods=['GET', 'POST'])
def handle_transcripts():
    """
    GET: List all transcripts with optional filtering
    POST: Create a new transcript and process it for insights
    """
    if request.method == 'GET':
        # Get query parameters for filtering
        client_name = request.args.get('client_name')
        processed = request.args.get('processed')
        
        query = Transcript.query
        
        if client_name:
            query = query.filter(Transcript.client_name.ilike(f'%{client_name}%'))
        
        if processed is not None:
            query = query.filter(Transcript.processed == (processed.lower() == 'true'))
        
        transcripts = query.order_by(Transcript.call_date.desc()).all()
        
        return jsonify({
            'success': True,
            'transcripts': [t.to_dict() for t in transcripts],
            'count': len(transcripts)
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Validate required fields
        if not data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: content'
            }), 400
        
        # Create new transcript
        transcript = Transcript(
            title=data.get('title', 'Untitled Transcript'),
            content=data.get('content'),
            client_name=data.get('client_name'),
            call_date=datetime.fromisoformat(data['call_date']) if 'call_date' in data else datetime.now(timezone.utc)
        )
        
        db.session.add(transcript)
        db.session.commit()
        
        # Process the transcript to extract insights
        try:
            insights_data = openai_service.extract_insights(transcript.content)
            
            for insight_data in insights_data:
                insight = Insight(
                    transcript_id=transcript.id,
                    category=insight_data['category'],
                    content=insight_data['content'],
                    sentiment=insight_data['sentiment'],
                    priority=insight_data['priority']
                )
                db.session.add(insight)
            
            transcript.processed = True
            db.session.commit()
            
            return jsonify({
                'success': True,
                'transcript': transcript.to_dict(),
                'message': f'Transcript created and {len(insights_data)} insights extracted'
            }), 201
            
        except Exception as e:
            # Even if insight extraction fails, keep the transcript
            db.session.commit()
            return jsonify({
                'success': True,
                'transcript': transcript.to_dict(),
                'warning': f'Transcript created but insight extraction failed: {str(e)}'
            }), 201


@app.route('/api/transcripts/<int:transcript_id>', methods=['GET', 'DELETE'])
def handle_transcript(transcript_id):
    """
    GET: Get a specific transcript with its insights
    DELETE: Delete a transcript
    """
    transcript = Transcript.query.get_or_404(transcript_id)
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'transcript': transcript.to_dict()
        })
    
    elif request.method == 'DELETE':
        db.session.delete(transcript)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transcript deleted successfully'
        })


@app.route('/api/insights', methods=['GET'])
def get_insights():
    """Get all insights with optional filtering"""
    category = request.args.get('category')
    sentiment = request.args.get('sentiment')
    priority = request.args.get('priority')
    
    query = Insight.query
    
    if category:
        query = query.filter(Insight.category == category)
    
    if sentiment:
        query = query.filter(Insight.sentiment == sentiment)
    
    if priority:
        query = query.filter(Insight.priority == priority)
    
    insights = query.order_by(Insight.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'insights': [i.to_dict() for i in insights],
        'count': len(insights)
    })


@app.route('/api/insights/summary', methods=['GET'])
def get_insights_summary():
    """Get a summary of all insights grouped by category"""
    insights = Insight.query.all()
    
    # Group by category
    summary = {}
    for insight in insights:
        category = insight.category
        if category not in summary:
            summary[category] = {
                'count': 0,
                'by_sentiment': {'positive': 0, 'negative': 0, 'neutral': 0},
                'by_priority': {'high': 0, 'medium': 0, 'low': 0}
            }
        
        summary[category]['count'] += 1
        
        sentiment = insight.sentiment or 'neutral'
        if sentiment in summary[category]['by_sentiment']:
            summary[category]['by_sentiment'][sentiment] += 1
        
        priority = insight.priority or 'medium'
        if priority in summary[category]['by_priority']:
            summary[category]['by_priority'][priority] += 1
    
    return jsonify({
        'success': True,
        'summary': summary,
        'total_insights': len(insights)
    })


@app.route('/api/process/<int:transcript_id>', methods=['POST'])
def process_transcript(transcript_id):
    """Manually trigger processing of a transcript"""
    transcript = Transcript.query.get_or_404(transcript_id)
    
    # Remove existing insights
    Insight.query.filter_by(transcript_id=transcript_id).delete()
    
    try:
        insights_data = openai_service.extract_insights(transcript.content)
        
        for insight_data in insights_data:
            insight = Insight(
                transcript_id=transcript.id,
                category=insight_data['category'],
                content=insight_data['content'],
                sentiment=insight_data['sentiment'],
                priority=insight_data['priority']
            )
            db.session.add(insight)
        
        transcript.processed = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(insights_data)} insights extracted',
            'transcript': transcript.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Database initialization
@app.before_request
def create_tables():
    """Create database tables before first request"""
    if not hasattr(app, '_tables_created'):
        db.create_all()
        app._tables_created = True


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# Quick Start Guide

Get up and running with the Transcript Insights Platform in 5 minutes!

## Prerequisites

- Python 3.8+
- Azure OpenAI account (optional for testing with sample data)

## Installation Steps

### 1. Clone and Setup

```bash
git clone https://github.com/HuxleyKendell/Transcriptting.git
cd Transcriptting
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI credentials:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
SECRET_KEY=your-random-secret-key
```

> **Note:** To test the application without Azure OpenAI, skip to step 4 and use sample data.

### 3. Initialize Database

```bash
python app.py
# Press Ctrl+C after you see "Running on http://127.0.0.1:5000"
```

### 4. Load Sample Data (Optional)

To test the application without Azure OpenAI credentials:

```bash
python sample_data.py
```

This creates 3 sample transcripts with 19 pre-extracted insights.

### 5. Start the Application

```bash
python app.py
```

Visit http://localhost:5000 in your browser.

## First Steps

### View the Dashboard

1. Open http://localhost:5000
2. The dashboard shows:
   - Total transcripts count
   - Total insights count
   - Feature requests and pain points
   - Detailed insights summary by category

### Upload a Transcript

1. Click the **"Upload Transcript"** tab
2. Fill in the form:
   - **Title**: e.g., "Sales Call with Acme Corp"
   - **Client Name**: e.g., "Acme Corp"
   - **Call Date**: Select date and time
   - **Content**: Paste the full transcript
3. Click **"Upload & Process"**
4. The system will automatically extract insights using Azure OpenAI

### Browse Transcripts

1. Click the **"Transcripts"** tab
2. See all transcripts with their extracted insights
3. Use the search box to filter by client name
4. Click **"View Details"** to see the full transcript
5. Click **"Delete"** to remove a transcript

### Filter Insights

1. Click the **"All Insights"** tab
2. Use the dropdown filters:
   - **Category**: Feature Requests, Pain Points, Positive Feedback, Concerns
   - **Sentiment**: Positive, Neutral, Negative
   - **Priority**: High, Medium, Low
3. View all matching insights across all transcripts

## Using the API

### Upload via API

```bash
curl -X POST http://localhost:5000/api/transcripts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Demo Call",
    "client_name": "Demo Client",
    "content": "Client mentioned they need better reporting..."
  }'
```

### Get All Insights

```bash
curl http://localhost:5000/api/insights/summary | python -m json.tool
```

### Filter Insights

```bash
curl "http://localhost:5000/api/insights?category=feature_request&priority=high"
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

## Integrating with Clari

### Option 1: Webhook Integration

Configure Clari to POST transcripts to:
```
http://your-server:5000/api/transcripts
```

### Option 2: Scheduled Import Script

Create a Python script that runs periodically:

```python
import requests

def fetch_and_upload_transcripts():
    # Fetch from Clari API
    clari_transcripts = fetch_from_clari_api()
    
    # Upload to Transcriptting
    for transcript in clari_transcripts:
        requests.post('http://localhost:5000/api/transcripts', json={
            'title': transcript['title'],
            'client_name': transcript['client'],
            'content': transcript['text'],
            'call_date': transcript['date']
        })

# Run every hour
schedule.every().hour.do(fetch_and_upload_transcripts)
```

### Option 3: Manual Upload

Use the web interface to paste transcript content from Clari.

## Production Deployment

### Using Gunicorn

```bash
gunicorn app:app --bind 0.0.0.0:8000 --workers 4
```

### Using Docker (create Dockerfile first)

```bash
docker build -t transcriptting .
docker run -p 8000:8000 --env-file .env transcriptting
```

### Environment Variables for Production

```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/dbname  # Use PostgreSQL
SECRET_KEY=generate-strong-random-key
```

## Troubleshooting

### "Azure OpenAI credentials not configured"

- Make sure `.env` file exists and has valid credentials
- Restart the application after updating `.env`
- Test without Azure OpenAI by using sample data

### Database errors

```bash
rm transcripts.db  # Delete old database
python app.py      # Recreate database
```

### Port already in use

```bash
# Use a different port
export PORT=8000
python app.py
```

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API usage
- Customize insight extraction in `openai_service.py`
- Deploy to production (Heroku, Azure, AWS, etc.)

## Support

For issues or questions, please open an issue on GitHub.

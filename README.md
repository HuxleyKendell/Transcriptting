# Transcriptting - Sales Call Transcript Insights Platform

A web application that automatically processes sales call transcripts from Clari and extracts product insights using Azure OpenAI. This tool helps product teams understand what clients really feel and want by collating insights from up to 50 daily transcripts into a single, easy-to-navigate dashboard.

## Features

- 📊 **Dashboard**: Real-time overview of all transcripts and insights
- 📝 **Transcript Management**: Upload, view, and manage sales call transcripts
- 🤖 **AI-Powered Analysis**: Automatically extract product insights using Azure OpenAI
- 💡 **Insight Categorization**: Insights are categorized into:
  - Feature Requests
  - Pain Points
  - Positive Feedback
  - Concerns
- 🎯 **Priority & Sentiment Analysis**: Each insight is tagged with priority level and sentiment
- 🔍 **Filtering & Search**: Filter insights by category, sentiment, and priority
- 📈 **Analytics**: View aggregated statistics and trends

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite (easily switchable to PostgreSQL/MySQL)
- **AI**: Azure OpenAI GPT models
- **Frontend**: Vanilla JavaScript with modern CSS
- **Deployment**: Gunicorn-ready for production

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI account with API key
- Git

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HuxleyKendell/Transcriptting.git
   cd Transcriptting
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Azure OpenAI credentials:
   ```
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   AZURE_OPENAI_API_VERSION=2023-05-15
   SECRET_KEY=your-secret-key-here
   ```

5. **Initialize the database**
   ```bash
   python app.py
   ```
   This will create the SQLite database with all necessary tables.

## Usage

### Running the Application

**Development Mode:**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

**Production Mode:**
```bash
gunicorn app:app --bind 0.0.0.0:8000
```

### Using the Web Interface

1. **Dashboard**: View overall statistics and insights summary
2. **Transcripts Tab**: View all uploaded transcripts and their extracted insights
3. **All Insights Tab**: Filter and browse all insights across all transcripts
4. **Upload Tab**: Upload new transcripts for processing

### API Endpoints

#### Transcripts

- `GET /api/transcripts` - List all transcripts
- `POST /api/transcripts` - Upload a new transcript
- `GET /api/transcripts/<id>` - Get specific transcript details
- `DELETE /api/transcripts/<id>` - Delete a transcript
- `POST /api/process/<id>` - Manually trigger processing

**Example: Upload a transcript**
```bash
curl -X POST http://localhost:5000/api/transcripts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sales Call with Acme Corp",
    "client_name": "Acme Corp",
    "content": "Full transcript text here...",
    "call_date": "2024-01-15T10:30:00"
  }'
```

#### Insights

- `GET /api/insights` - List all insights (with optional filters)
- `GET /api/insights/summary` - Get insights summary grouped by category

**Example: Get feature requests**
```bash
curl "http://localhost:5000/api/insights?category=feature_request&priority=high"
```

## Integration with Clari

To automatically push transcripts from Clari to this platform, you can:

1. **Webhook Integration**: Configure Clari to send transcripts to your `/api/transcripts` endpoint
2. **Scheduled Import**: Create a script that periodically fetches transcripts from Clari's API and posts them to this platform
3. **Manual Upload**: Use the web interface to paste transcript content

### Example Integration Script

```python
import requests
import os

def upload_transcript(title, content, client_name=None, call_date=None):
    url = "http://your-server:5000/api/transcripts"
    payload = {
        "title": title,
        "content": content,
        "client_name": client_name,
        "call_date": call_date
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# Example usage
result = upload_transcript(
    title="Sales Call - Q4 2024",
    content="Transcript content here...",
    client_name="Example Corp",
    call_date="2024-01-15T14:30:00"
)
print(result)
```

## Database Schema

### Transcripts Table
- `id`: Primary key
- `title`: Transcript title
- `content`: Full transcript text
- `call_date`: Date of the sales call
- `client_name`: Name of the client
- `created_at`: When the transcript was uploaded
- `processed`: Whether insights have been extracted

### Insights Table
- `id`: Primary key
- `transcript_id`: Foreign key to transcripts
- `category`: Type of insight (feature_request, pain_point, etc.)
- `content`: The insight text
- `sentiment`: Positive, negative, or neutral
- `priority`: High, medium, or low
- `created_at`: When the insight was created

## Customization

### Changing the Database

To use PostgreSQL or MySQL instead of SQLite, update the `DATABASE_URL` in your `.env` file:

**PostgreSQL:**
```
DATABASE_URL=postgresql://user:password@localhost/transcriptting
```

**MySQL:**
```
DATABASE_URL=mysql://user:password@localhost/transcriptting
```

### Customizing Insight Extraction

Edit `openai_service.py` to modify the system prompt and adjust how insights are extracted. You can:
- Add new insight categories
- Change priority/sentiment analysis criteria
- Adjust the AI model parameters (temperature, max_tokens)

## Deployment

### Deploy to Cloud Platforms

**Heroku:**
```bash
heroku create your-app-name
heroku config:set AZURE_OPENAI_ENDPOINT=your-endpoint
heroku config:set AZURE_OPENAI_API_KEY=your-key
heroku config:set AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
git push heroku main
```

**Azure App Service:**
```bash
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myUniqueAppName --runtime "PYTHON|3.11"
az webapp config appsettings set --resource-group myResourceGroup --name myUniqueAppName --settings @appsettings.json
```

**Docker:**
A Dockerfile can be added for containerized deployment.

## Troubleshooting

### Common Issues

1. **"Azure OpenAI credentials not configured"**
   - Make sure your `.env` file has the correct Azure OpenAI settings
   - Verify the endpoint URL doesn't have a trailing slash

2. **"Failed to extract insights"**
   - Check that your Azure OpenAI deployment is active
   - Verify the API key has proper permissions
   - Ensure the deployment name matches your Azure configuration

3. **Database errors**
   - Delete the `transcripts.db` file and restart the app to recreate the database
   - Check file permissions in the application directory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for your own purposes.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
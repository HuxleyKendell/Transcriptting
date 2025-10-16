# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### Transcripts

#### List All Transcripts
```http
GET /api/transcripts
```

**Query Parameters:**
- `client_name` (optional): Filter by client name (partial match)
- `processed` (optional): Filter by processing status (`true` or `false`)

**Response:**
```json
{
  "success": true,
  "count": 3,
  "transcripts": [
    {
      "id": 1,
      "title": "Sales Call - Example Corp",
      "content": "Full transcript text...",
      "call_date": "2024-01-15T14:30:00",
      "client_name": "Example Corp",
      "created_at": "2024-01-15T14:35:00",
      "processed": true,
      "insights": [...]
    }
  ]
}
```

#### Create New Transcript
```http
POST /api/transcripts
```

**Request Body:**
```json
{
  "title": "Sales Call - Example Corp",
  "content": "Full transcript text here...",
  "client_name": "Example Corp",
  "call_date": "2024-01-15T14:30:00"
}
```

**Response:**
```json
{
  "success": true,
  "transcript": {...},
  "message": "Transcript created and 5 insights extracted"
}
```

#### Get Specific Transcript
```http
GET /api/transcripts/:id
```

**Response:**
```json
{
  "success": true,
  "transcript": {
    "id": 1,
    "title": "...",
    "content": "...",
    "insights": [...]
  }
}
```

#### Delete Transcript
```http
DELETE /api/transcripts/:id
```

**Response:**
```json
{
  "success": true,
  "message": "Transcript deleted successfully"
}
```

#### Process/Reprocess Transcript
```http
POST /api/process/:id
```

**Response:**
```json
{
  "success": true,
  "message": "5 insights extracted",
  "transcript": {...}
}
```

### Insights

#### List All Insights
```http
GET /api/insights
```

**Query Parameters:**
- `category` (optional): Filter by category (`feature_request`, `pain_point`, `positive_feedback`, `concern`)
- `sentiment` (optional): Filter by sentiment (`positive`, `negative`, `neutral`)
- `priority` (optional): Filter by priority (`high`, `medium`, `low`)

**Response:**
```json
{
  "success": true,
  "count": 15,
  "insights": [
    {
      "id": 1,
      "transcript_id": 1,
      "category": "feature_request",
      "content": "Need better reporting capabilities",
      "sentiment": "neutral",
      "priority": "high",
      "created_at": "2024-01-15T14:35:00"
    }
  ]
}
```

#### Get Insights Summary
```http
GET /api/insights/summary
```

**Response:**
```json
{
  "success": true,
  "total_insights": 19,
  "summary": {
    "feature_request": {
      "count": 8,
      "by_sentiment": {
        "positive": 0,
        "negative": 0,
        "neutral": 8
      },
      "by_priority": {
        "high": 4,
        "medium": 4,
        "low": 0
      }
    },
    "pain_point": {...},
    "positive_feedback": {...},
    "concern": {...}
  }
}
```

## Example Usage

### Python

```python
import requests

# Upload a transcript
response = requests.post('http://localhost:5000/api/transcripts', json={
    'title': 'Sales Call with TechCorp',
    'client_name': 'TechCorp',
    'content': 'Full transcript text here...',
    'call_date': '2024-01-15T14:30:00'
})

result = response.json()
print(f"Transcript ID: {result['transcript']['id']}")

# Get all feature requests
response = requests.get('http://localhost:5000/api/insights', params={
    'category': 'feature_request',
    'priority': 'high'
})

insights = response.json()['insights']
for insight in insights:
    print(f"- {insight['content']}")
```

### cURL

```bash
# Upload a transcript
curl -X POST http://localhost:5000/api/transcripts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sales Call with TechCorp",
    "client_name": "TechCorp",
    "content": "Full transcript text...",
    "call_date": "2024-01-15T14:30:00"
  }'

# Get insights summary
curl http://localhost:5000/api/insights/summary

# Filter insights by category
curl "http://localhost:5000/api/insights?category=feature_request&priority=high"
```

### JavaScript

```javascript
// Upload a transcript
const response = await fetch('http://localhost:5000/api/transcripts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'Sales Call with TechCorp',
    client_name: 'TechCorp',
    content: 'Full transcript text...',
    call_date: '2024-01-15T14:30:00'
  })
});

const result = await response.json();
console.log('Transcript ID:', result.transcript.id);

// Get all insights
const insightsResponse = await fetch('http://localhost:5000/api/insights');
const insightsData = await insightsResponse.json();
console.log('Total insights:', insightsData.count);
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful GET/DELETE request
- `201 Created`: Successful POST request
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "success": false,
  "error": "Error message here"
}
```

import json
from openai import AzureOpenAI
from config import Config

class OpenAIService:
    """Service for interacting with Azure OpenAI to extract insights from transcripts"""
    
    def __init__(self):
        """Initialize Azure OpenAI client"""
        self.client = None
        self.deployment_name = Config.AZURE_OPENAI_DEPLOYMENT_NAME
    
    def _ensure_client(self):
        """Lazy initialization of Azure OpenAI client"""
        if self.client is None:
            if not Config.AZURE_OPENAI_ENDPOINT or not Config.AZURE_OPENAI_API_KEY:
                raise ValueError("Azure OpenAI credentials not configured. Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in .env file.")
            
            self.client = AzureOpenAI(
                azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
                api_key=Config.AZURE_OPENAI_API_KEY,
                api_version=Config.AZURE_OPENAI_API_VERSION
            )
    
    def extract_insights(self, transcript_content):
        """
        Extract product insights from a transcript using Azure OpenAI
        
        Args:
            transcript_content: The transcript text to analyze
            
        Returns:
            List of insights dictionaries with keys: category, content, sentiment, priority
        """
        self._ensure_client()
        
        system_prompt = """You are an expert at analyzing sales call transcripts to extract product insights.
Your task is to identify and extract:
1. Feature requests - specific features or capabilities clients want
2. Pain points - problems or frustrations clients are experiencing
3. Positive feedback - things clients like or appreciate
4. Concerns - worries or objections clients have

For each insight, provide:
- category: One of 'feature_request', 'pain_point', 'positive_feedback', or 'concern'
- content: A clear, concise summary of the insight
- sentiment: 'positive', 'negative', or 'neutral'
- priority: 'high', 'medium', or 'low' based on the emphasis and importance in the conversation

Return the results as a JSON array of objects with these fields."""

        user_prompt = f"""Analyze the following sales call transcript and extract all product insights:

{transcript_content}

Please provide the insights in JSON format as an array of objects."""

        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract the response content
            response_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON from the response
            # Sometimes the model wraps JSON in markdown code blocks
            if response_text.startswith('```'):
                # Remove markdown code blocks
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else response_text
                if response_text.startswith('json'):
                    response_text = response_text[4:].strip()
            
            insights = json.loads(response_text)
            
            # Validate and normalize the insights
            normalized_insights = []
            for insight in insights:
                if isinstance(insight, dict) and 'category' in insight and 'content' in insight:
                    normalized_insights.append({
                        'category': insight.get('category', 'other'),
                        'content': insight.get('content', ''),
                        'sentiment': insight.get('sentiment', 'neutral'),
                        'priority': insight.get('priority', 'medium')
                    })
            
            return normalized_insights
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from OpenAI response: {e}")
            print(f"Response was: {response_text}")
            return []
        except Exception as e:
            print(f"Error extracting insights: {e}")
            return []
    
    def summarize_insights(self, insights):
        """
        Generate a high-level summary of multiple insights
        
        Args:
            insights: List of insight dictionaries
            
        Returns:
            A summary string
        """
        if not insights:
            return "No insights available."
        
        # Group insights by category
        by_category = {}
        for insight in insights:
            category = insight.get('category', 'other')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(insight.get('content', ''))
        
        # Create a summary
        summary_parts = []
        for category, items in by_category.items():
            summary_parts.append(f"{category.replace('_', ' ').title()}: {len(items)} items")
        
        return " | ".join(summary_parts)

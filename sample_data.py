"""
Sample data script to populate the database with example transcripts for testing.
This is useful for demonstrating the application without needing Azure OpenAI credentials.
"""
from datetime import datetime, timedelta, timezone
from app import app, db
from models import Transcript, Insight

def create_sample_data():
    """Create sample transcripts and insights"""
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Insight.query.delete()
        Transcript.query.delete()
        db.session.commit()
        
        # Sample transcript 1
        transcript1 = Transcript(
            title="Discovery Call - TechCorp Solutions",
            client_name="TechCorp Solutions",
            call_date=datetime.now(timezone.utc) - timedelta(days=2),
            content="""
            Sales Rep: Thanks for joining us today. Can you tell me about your current workflow?
            
            Client: We're using spreadsheets to manage everything, and it's becoming really difficult. 
            Our team has grown to 50 people and we're losing track of important information. 
            We need a better system for collaboration.
            
            Sales Rep: What features are most important to you?
            
            Client: Real-time collaboration is critical. We also need better reporting capabilities 
            and mobile access. Our sales team is always on the go. The pricing seems reasonable, 
            but we'd love to see a bulk discount option.
            
            Sales Rep: How are you handling data security right now?
            
            Client: That's actually a major concern. We're dealing with sensitive client information 
            and need enterprise-grade security. GDPR compliance is a must for us.
            """,
            processed=True
        )
        db.session.add(transcript1)
        db.session.flush()
        
        # Add insights for transcript 1
        insights1 = [
            Insight(
                transcript_id=transcript1.id,
                category='pain_point',
                content='Current spreadsheet-based workflow is difficult to manage with 50-person team',
                sentiment='negative',
                priority='high'
            ),
            Insight(
                transcript_id=transcript1.id,
                category='feature_request',
                content='Real-time collaboration capabilities',
                sentiment='neutral',
                priority='high'
            ),
            Insight(
                transcript_id=transcript1.id,
                category='feature_request',
                content='Better reporting capabilities',
                sentiment='neutral',
                priority='medium'
            ),
            Insight(
                transcript_id=transcript1.id,
                category='feature_request',
                content='Mobile access for sales team on the go',
                sentiment='neutral',
                priority='high'
            ),
            Insight(
                transcript_id=transcript1.id,
                category='concern',
                content='Data security and GDPR compliance for sensitive client information',
                sentiment='negative',
                priority='high'
            ),
            Insight(
                transcript_id=transcript1.id,
                category='positive_feedback',
                content='Pricing seems reasonable',
                sentiment='positive',
                priority='low'
            ),
            Insight(
                transcript_id=transcript1.id,
                category='feature_request',
                content='Bulk discount option for pricing',
                sentiment='neutral',
                priority='medium'
            )
        ]
        
        for insight in insights1:
            db.session.add(insight)
        
        # Sample transcript 2
        transcript2 = Transcript(
            title="Follow-up Call - FinanceFlow Inc",
            client_name="FinanceFlow Inc",
            call_date=datetime.now(timezone.utc) - timedelta(days=5),
            content="""
            Sales Rep: Thanks for the follow-up. Have you had a chance to try the demo?
            
            Client: Yes! We really like the user interface. It's very intuitive and our team 
            picked it up quickly. The onboarding process was smooth.
            
            Sales Rep: That's great to hear! Any concerns?
            
            Client: We need better integration with our existing CRM system. Currently, we're 
            using Salesforce and it would be great if your product could sync automatically. 
            Also, the export functionality is limited - we need to export to more formats like 
            CSV, Excel, and PDF.
            
            Sales Rep: Understood. Anything else?
            
            Client: The customer support has been fantastic. Very responsive and helpful. 
            We'd like to see more customization options for dashboards though. Each department 
            has different metrics they want to track.
            """,
            processed=True
        )
        db.session.add(transcript2)
        db.session.flush()
        
        # Add insights for transcript 2
        insights2 = [
            Insight(
                transcript_id=transcript2.id,
                category='positive_feedback',
                content='Intuitive user interface that team picked up quickly',
                sentiment='positive',
                priority='low'
            ),
            Insight(
                transcript_id=transcript2.id,
                category='positive_feedback',
                content='Smooth onboarding process',
                sentiment='positive',
                priority='low'
            ),
            Insight(
                transcript_id=transcript2.id,
                category='feature_request',
                content='Integration with Salesforce CRM for automatic syncing',
                sentiment='neutral',
                priority='high'
            ),
            Insight(
                transcript_id=transcript2.id,
                category='feature_request',
                content='Enhanced export functionality supporting CSV, Excel, and PDF formats',
                sentiment='neutral',
                priority='medium'
            ),
            Insight(
                transcript_id=transcript2.id,
                category='positive_feedback',
                content='Fantastic and responsive customer support',
                sentiment='positive',
                priority='low'
            ),
            Insight(
                transcript_id=transcript2.id,
                category='feature_request',
                content='More customization options for dashboards to track department-specific metrics',
                sentiment='neutral',
                priority='medium'
            )
        ]
        
        for insight in insights2:
            db.session.add(insight)
        
        # Sample transcript 3
        transcript3 = Transcript(
            title="Quarterly Review - DataDrive Systems",
            client_name="DataDrive Systems",
            call_date=datetime.now(timezone.utc) - timedelta(days=10),
            content="""
            Sales Rep: How has your experience been over the past quarter?
            
            Client: Overall, we're satisfied. The product does what we need it to do. 
            Performance has been solid, no major outages.
            
            Sales Rep: Any areas where we can improve?
            
            Client: The loading times for large datasets could be faster. We're dealing with 
            millions of rows and it can take a while. Also, the search functionality doesn't 
            always return relevant results. We've had to create workarounds.
            
            Sales Rep: I see. Anything else?
            
            Client: We'd love an API to integrate with our internal tools. Right now everything 
            is manual and it's time-consuming. Better documentation would help too - sometimes 
            we have to contact support for things that should be in the docs.
            """,
            processed=True
        )
        db.session.add(transcript3)
        db.session.flush()
        
        # Add insights for transcript 3
        insights3 = [
            Insight(
                transcript_id=transcript3.id,
                category='positive_feedback',
                content='Overall satisfaction with product functionality',
                sentiment='positive',
                priority='low'
            ),
            Insight(
                transcript_id=transcript3.id,
                category='positive_feedback',
                content='Solid performance with no major outages',
                sentiment='positive',
                priority='low'
            ),
            Insight(
                transcript_id=transcript3.id,
                category='pain_point',
                content='Slow loading times for large datasets with millions of rows',
                sentiment='negative',
                priority='high'
            ),
            Insight(
                transcript_id=transcript3.id,
                category='pain_point',
                content='Search functionality not returning relevant results, requiring workarounds',
                sentiment='negative',
                priority='high'
            ),
            Insight(
                transcript_id=transcript3.id,
                category='feature_request',
                content='API for integration with internal tools to reduce manual work',
                sentiment='neutral',
                priority='high'
            ),
            Insight(
                transcript_id=transcript3.id,
                category='pain_point',
                content='Incomplete documentation requiring support contact for basic information',
                sentiment='negative',
                priority='medium'
            )
        ]
        
        for insight in insights3:
            db.session.add(insight)
        
        # Commit all changes
        db.session.commit()
        
        print(f"Created {Transcript.query.count()} transcripts")
        print(f"Created {Insight.query.count()} insights")
        print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()

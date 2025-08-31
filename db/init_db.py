import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from dotenv import load_dotenv
from db.database import SessionLocal, Base
from db.models.models import FAQ
from api.models import Feedback, ContentLog, CustomerScore, Mention

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def init_database():
    engine = create_engine(DATABASE_URL)

    # Create tables first
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

    # Insert some sample FAQs
    try:
        with SessionLocal() as session:
            # Check if FAQs already exist
            existing_faqs = session.query(FAQ).count()
            if existing_faqs == 0:
                sample_faqs = [
                    FAQ(
                        question="What are your business hours?",
                        answer="We are open Monday to Friday from 9 AM to 6 PM.",
                        keywords=['hours', 'open', 'time', 'schedule']
                    ),
                    FAQ(
                        question="How can I contact support?",
                        answer="You can reach our support team at support@example.com or call 1-800-123-4567.",
                        keywords=['contact', 'support', 'help', 'email', 'phone']
                    ),
                    FAQ(
                        question="What payment methods do you accept?",
                        answer="We accept credit cards, PayPal, and bank transfers.",
                        keywords=['payment', 'pay', 'credit', 'paypal', 'bank']
                    ),
                    FAQ(
                        question="How do I return a product?",
                        answer="Returns can be processed within 30 days of purchase with original receipt.",
                        keywords=['return', 'refund', 'exchange', 'product']
                    )
                ]

                for faq in sample_faqs:
                    session.add(faq)
                session.commit()
                print("Sample FAQs inserted successfully!")
            else:
                print(f"FAQs already exist ({existing_faqs} found)")
    except Exception as e:
        print(f"Error inserting sample data: {e}")

    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()

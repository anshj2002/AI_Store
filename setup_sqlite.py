#!/usr/bin/env python3
"""
SQLite Database Setup for AI Suite
Initializes the SQLite database with all required tables and sample data
"""

import os
import sys
from sqlalchemy import create_engine, text
from db.database import Base, SQLALCHEMY_DATABASE_URL
import db.models.models  # Import to register models with Base
import api.models  # Import additional models

def create_database():
    """Create SQLite database and tables"""

    # Ensure database directory exists
    db_dir = os.path.dirname(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))
    os.makedirs(db_dir, exist_ok=True)

    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

    # Create all tables from SQLAlchemy models
    print("📝 Creating database tables...")
    Base.metadata.create_all(bind=engine)

    # Insert sample data
    print("📥 Inserting sample data...")
    with engine.connect() as conn:
        # Sample FAQs
        sample_faqs = [
            (1, "What are your business hours?", "We are open Monday to Friday from 9 AM to 6 PM.", '["hours","open","time","schedule"]'),
            (2, "How can I contact support?", "You can reach our support team at support@example.com or call 1-800-123-4567.", '["contact","support","help","email","phone"]'),
            (3, "What payment methods do you accept?", "We accept credit cards, PayPal, and bank transfers.", '["payment","pay","credit","paypal","bank"]'),
            (4, "How do I return a product?", "Returns can be processed within 30 days of purchase with original receipt.", '["return","refund","exchange","product"]')
        ]

        for faq_id, question, answer, keywords in sample_faqs:
            conn.execute(text("""
                INSERT OR REPLACE INTO faqs (id, question, answer, keywords)
                VALUES (:id, :question, :answer, :keywords)
            """), {
                "id": faq_id,
                "question": question,
                "answer": answer,
                "keywords": keywords
            })

        conn.commit()

    print("✅ Database setup complete!")
    print(f"📍 Database location: {SQLALCHEMY_DATABASE_URL.replace('sqlite:///', '')}")

def test_database():
    """Test database connection and show tables"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    print("\n🧪 Testing database connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result.fetchall()]

            print(f"✅ Connected successfully!")
            print("📋 Tables created:")
            for table in tables:
                print(f"   • {table}")

            # Count FAQs
            faq_count = conn.execute(text("SELECT COUNT(*) FROM faqs")).fetchone()[0]
            print(f"📚 Sample FAQs loaded: {faq_count}")

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

    return True

def main():
    """Main setup function"""
    print("🚀 AI Suite - SQLite Database Setup")
    print("=" * 40)

    try:
        create_database()
        if test_database():
            print("\n🎉 Setup successful!")
            print("\n📋 Next steps:")
            print("1. Run: uvicorn api.main:app --reload")
            print("2. Open: http://127.0.0.1:8000/docs")
            print("3. Test chat: curl -X POST http://127.0.0.1:8000/chat -H 'Content-Type: application/json' -d '{\"message\":\"What are your hours?\"}'")
            print("4. Open web/chat.html in browser")
        else:
            print("\n❌ Setup failed!")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

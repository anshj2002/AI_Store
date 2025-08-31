import os
import sys
from sqlalchemy import create_engine

# SQLite database configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "customer_ai.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

def create_database():
    """Create SQLite database file"""

    # Ensure database directory exists
    db_dir = os.path.dirname(DB_PATH)
    os.makedirs(db_dir, exist_ok=True)

    # Create engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

    # Read and execute SQL schema
    schema_path = os.path.join(BASE_DIR, "db", "init.sql")
    if os.path.exists(schema_path):
        print("📝 Creating database tables from schema...")

        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        # Split into individual statements and execute
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]

        with engine.connect() as conn:
            for statement in statements:
                if statement:
                    try:
                        conn.execute(statement)
                        conn.commit()
                    except Exception as e:
                        print(f"Warning: {e}")
    else:
        print("❌ Schema file not found!")

    print("✅ Database setup complete!")
    print(f"📍 Database location: {DB_PATH}")

def test_database():
    """Test database connection"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    print("\n🧪 Testing database connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in result.fetchall()]

            print(f"✅ Connected successfully!")
            print("📋 Tables created:")
            for table in tables:
                print(f"   • {table}")

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

    return True

def main():
    """Main setup function"""
    print("🚀 AI Suite - Simple SQLite Setup")
    print("=" * 35)

    try:
        create_database()
        if test_database():
            print("\n🎉 Setup successful!")
            print("\n📋 Next steps:")
            print("1. Run: uvicorn api.main:app --reload")
            print("2. Open: http://127.0.0.1:8000/docs")
            print("3. Test with: curl -X POST http://127.0.0.1:8000/chat -H 'Content-Type: application/json' -d '{\"message\":\"test\"}'")
        else:
            print("\n❌ Setup failed!")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

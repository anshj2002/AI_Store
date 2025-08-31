from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import SQLALCHEMY_DATABASE_URL, Base
import api.models  # Import models
from api.models import FAQ

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

faqs = session.query(FAQ).all()
print(f"Number of FAQs: {len(faqs)}")
for faq in faqs:
    print(f"Question: {faq.question}")
    print(f"Keywords: {faq.keywords}")
    print(f"Keywords list: {faq.keywords_list}")
    print(f"Answer: {faq.answer}")
    print("---")

session.close()

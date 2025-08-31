import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///customer_ai.db")

    # App settings
    APP_NAME: str = os.getenv("APP_NAME", "Mini Customer AI")
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

    # Brand settings
    BRAND_NAME: str = os.getenv("BRAND_NAME", "MYAISTORE")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.55"))

    # Analytics
    CUSTOMERS_CSV: str = os.getenv("CUSTOMERS_CSV", "/data/customers.csv")

    # Debug
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

settings = Settings()

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "FoodLoop"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Google Cloud & Vertex AI
    GCP_PROJECT_ID: str = "foodloop-hackathon"
    GCP_LOCATION: str = "asia-south1"
    VERTEX_AI_MODEL_FLASH: str = "gemini-2.5-flash"
    VERTEX_AI_MODEL_PRO: str = "gemini-1.5-pro"
    
    # Firebase & Auth
    FIREBASE_PROJECT_ID: str = "foodloop-hackathon"
    SECRET_KEY: str = "insecure-dev-secret-key-change-in-prod"
    APP_CHECK_ENABLED: bool = False
    
    # BigQuery
    BIGQUERY_DATASET: str = "foodloop_analytics"
    
    # Operational constraints
    MATCHING_RADIUS_KM: float = 5.0
    FSSAI_MAX_AMBIENT_HOURS: float = 4.0
    FSSAI_HIGH_HEAT_MAX_HOURS: float = 2.0
    HIGH_HEAT_TEMP_THRESHOLD_C: float = 32.0

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()

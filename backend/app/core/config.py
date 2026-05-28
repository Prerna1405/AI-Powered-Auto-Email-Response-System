from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI-Powered Automatic Email Response System"
    environment: str = "development"

    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/auto_email"
    redis_url: str = "redis://redis:6379/0"
    openai_api_key: str = ""

    support_email: str = "support@company.com"
    company_name: str = "Acme"
    reset_url: str = "https://example.com/reset-password"
    confidence_threshold: int = 75
    auto_reply_enabled: bool = True
    email_poll_interval_seconds: int = 60

    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    gmail_refresh_token: str = ""
    gmail_connected: bool = False

    # Email delivery
    email_delivery_mode: str = "simulator"
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_user: str = ""
    smtp_password: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

from pydantic import BaseSettings

description = """
Site Builder is an application to create websites without any coding knowledge.

Although you can create complex functionality if you have coding skills but for 
a normal user this should be an easy to use tool for creating websites.
"""


class Settings(BaseSettings):
    env: str = "Development"  # or "Production"
    app_name: str = "Site Builder API"
    description: str = description
    version: str = "0.1.0"
    terms_of_service: str = ""
    contact_person: str = "Sazedul Islam"
    contact_email: str = "sazidmailbox@gmail.com"
    mongodb_url: str = "mongodb+srv://sbuser:sbdbuser@dev.4vobw.mongodb.net/sbdb?retryWrites=true&w=majority"
    mongodb_db_name: str = "sbdb"
    # to get a string like this run:
    # openssl rand -hex 32
    secret_key: str = "secret_key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 3600
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "DEBUG"
    json_logs: bool = False
    log_path: str = "logs"
    log_file: str = "log"
    workers: int = 4

    origins = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]

    class Config:
        env_file: str = ".env"


settings = Settings()

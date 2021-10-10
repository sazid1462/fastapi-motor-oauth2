from pydantic import BaseSettings

description = """
Site Builder is an application to create websites without any coding knowledge.

Although you can create complex functionality if you have coding skills but for 
a normal user this should be an easy to use tool for creating websites.
"""


class Settings(BaseSettings):
    app_name: str = "Site Builder API"
    description: str = description
    version: str = "0.1.0"
    terms_of_service: str = ""
    contact_person: str = "Sazedul Islam"
    contact_email: str = "sazidmailbox@gmail.com"
    mongodb_url: str = "mongodb+srv://sbuser:sbdbuser@dev.4vobw.mongodb.net/sbdb?retryWrites=true&w=majority"
    # to get a string like this run:
    # openssl rand -hex 32
    secret_key: str = "30855ff5d6a40ec61b05eefa0d6107f43e4a60de474e2adacd075a9c9211345e"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes = 30

    origins = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]

    class Config:
        env_file: str = ".env"


settings = Settings()

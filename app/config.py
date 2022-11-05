from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    1. Retrieve the environment variables from computer.
    2. Convert into lowercase.
    3. Validate with type hint.
    """
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        """Read data from .env file"""
        env_file = "app/.env"


settings = Settings()
if __name__ == "__main__":
    user_name = settings.database_username
    user_password = settings.database_password
    hostname = settings.database_hostname
    port = settings.database_port
    database_name = settings.database_name

    path= f"postgresql://{user_name}:{user_password}@{hostname}/{database_name}"
    print(path)
    print(settings.algorithm)
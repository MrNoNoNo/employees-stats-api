from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent
    data_path: Path = base_dir / "data" / "data.json"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
DATA_PATH = settings.data_path

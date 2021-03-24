import os
from typing import Optional

from pydantic import BaseModel, BaseSettings, Field


class AppConfig(BaseModel):
    """Application configurations."""

    DB: str = "Area51"


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # These variables will be loaded from the .env file. However, if
    # there is a shell environment variable having the same name,
    # that will take precedence.

    APP_CONFIG: AppConfig = AppConfig()

    # define global variables with the Field class
    ENV_STATE: Optional[str] = Field(None, env="ENV_STATE")

    # environment specific variables do not need the Field class
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None
    REDIS_PASS: Optional[str] = None

    DATASETS_BASE_PATH: Optional[str] = os.path.expanduser("~/.datasets")
    WORKSPACES_BASE_PATH: Optional[str] = os.path.expanduser("~/.workspaces")
    TRASH_BASE_PATH: Optional[str] = os.path.expanduser("~/.trash")
    IMAGES_FOLDER: Optional[str] = "images"
    VALIDATION_FOLDER: Optional[str] = "validation_images"
    MODELS_FOLDER: Optional[str] = "models"

    class Config:
        """Loads the dotenv file."""

        env_file: str = ".env"


class DevConfig(GlobalConfig):
    """Development configurations."""

    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "PROD_"


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state.lower() if type(env_state) == str else "dev"

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


cnf = FactoryConfig(GlobalConfig().ENV_STATE)()


if __name__ == "__main__":
    print(cnf.__repr__())
    print(cnf.__dir__())

import os
from pathlib import Path

from pydantic import BaseSettings


class Configs(BaseSettings):

    class Config:
        root_dir_path: str = os.path.join(
            Path(__file__).parent.parent.parent.absolute()
        )
        env_file: str = os.path.join(root_dir_path, "env", ".env")
        env_file_encoding: str = "utf-8"

    ENV: str
    LOGGER_CONFIG_PATH: str = os.path.join(
        Config.root_dir_path, "src", "logger_config.yaml"
    )


configs = Configs()

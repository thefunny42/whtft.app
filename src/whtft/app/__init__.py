import importlib.resources
import pathlib

import fastapi
import pydantic
import pydantic_settings
import uvicorn

__version__ = "0.1.0"

DEFAULT_LOG_CONFIG = pathlib.Path(
    str(importlib.resources.files("whtft.app") / "logging.yaml")
)


class Settings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        secrets_dir="/app/conf",
    )

    default_log_config: pydantic.FilePath | None = pydantic.Field(
        default=DEFAULT_LOG_CONFIG
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[pydantic_settings.BaseSettings],
        init_settings: pydantic_settings.PydanticBaseSettingsSource,
        env_settings: pydantic_settings.PydanticBaseSettingsSource,
        dotenv_settings: pydantic_settings.PydanticBaseSettingsSource,
        file_secret_settings: pydantic_settings.PydanticBaseSettingsSource,
    ) -> tuple[pydantic_settings.PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            file_secret_settings,
            env_settings,
            dotenv_settings,
        )


def main(app: fastapi.FastAPI, settings: Settings):  # pragma: no cover
    log_config = None
    if settings.default_log_config is not None:
        log_config = str(settings.default_log_config)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        server_header=False,
        log_config=log_config,
    )

from openg2p_fastapi_common.config import Settings
from pydantic_settings import SettingsConfigDict


class Settings(Settings):
    model_config = SettingsConfigDict(
        env_prefix="portal_", env_file=".env", extra="allow"
    )

    openapi_title: str = "G2P Portal API"
    openapi_description: str = """
    This module implements G2P Portal APIs.

    ***********************************
    Further details goes here
    ***********************************
    """

    openapi_version: str = "0.1.0"

import os

from dotenv import load_dotenv
from pydantic import BaseModel


class APIConfig(BaseModel):
    BASE_URL: str
    DEBUG: bool


class ClientConfig(BaseModel):
    api: APIConfig


def get_config() -> ClientConfig:
    debug = os.environ.get("DEBUG", default="true").lower() == "true"

    if debug:
        load_dotenv()

    return ClientConfig(
        api=APIConfig(
            BASE_URL=os.environ.get("BASE_URL"),
            DEBUG=os.environ.get("DEBUG").lower() == "true",
        )
    )

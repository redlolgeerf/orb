from pydantic_settings import BaseSettings
from pydantic import (
    AnyHttpUrl,
)


class Settings(BaseSettings):
    messages_service_url: AnyHttpUrl = (
        "https://owpublic.blob.core.windows.net/tech-task/messages"
    )
    reports_service_url: AnyHttpUrl = (
        "https://owpublic.blob.core.windows.net/tech-task/reports"
    )


SETTINGS = Settings()

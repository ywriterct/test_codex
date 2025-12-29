import os


class Settings:
    def __init__(self) -> None:
        self.mta_api_key = os.getenv("MTA_API_KEY", "")
        self.mta_feed_url = os.getenv(
            "MTA_FEED_URL",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
        )
        self.mta_api_key_header = os.getenv("MTA_API_KEY_HEADER", "x-api-key")
        self.request_timeout_seconds = float(
            os.getenv("MTA_REQUEST_TIMEOUT_SECONDS", "10")
        )


settings = Settings()

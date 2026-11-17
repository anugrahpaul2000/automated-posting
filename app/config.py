from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mastodon_base_url: str = "https://mastodon.social"
    mastodon_token: str = ""
    bluesky_handle: str = ""
    bluesky_app_password: str = ""
    devto_api_key: str = ""
    telegram_bot_token: str = ""
    telegram_channel: str = ""
    discord_webhook_url: str = ""


settings = Settings()

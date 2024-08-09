from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	DB_HOST: str
	DB_PORT: int
	DB_NAME: str
	DB_USER: str
	DB_PASSWORD: str
	SECRET_KEY_FOR_JWT: str

	@property
	def db_url_asyncpg(self):
		return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

	@property
	def db_url_psycopg(self):
		return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

	model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

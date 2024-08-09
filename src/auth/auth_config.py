from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy

from src.config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY_FOR_JWT, lifetime_seconds=3600)


cookie_transport = CookieTransport(cookie_name="technical_blog")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
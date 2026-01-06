
import pkce
from modals.config import Envs
from modals.oauth import OAuthRequest
from utils.sessions import AuthSession


class OAuthClient:
    """Авториизует по Oauth2.0"""

    session: AuthSession
    base_url: str

    def __init__(self, env: Envs):
        """Генерируем code_verifier и code_challenge. И генерируем basic auth token из секрета сервиса авторизации."""
        self.session = AuthSession(base_url=env.auth_url)
        self.redirect_uri = env.frontend_url + "/authorized"
        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair()
        self.token = None

    def get_token(self, username, password):
        """Возвраащает token oauth для авторизации пользователя с username и password
        1. Получаем jsessionid и xsrf-token куку в сесссию.
        2. Получаем code из redirec по xsrf-token'у.
        3. Получаем access_token.
        """
        self.session.get(
            url="/oauth2/authorize",
            params=OAuthRequest(
                redirect_uri=self.redirect_uri,
                code_challenge=self.code_challenge
            ).model_dump(),
            allow_redirects=True
        )

        self.session.post(
            url="/login",
            data={
                "username": username,
                "password": password,
                "_csrf": self.session.cookies.get("XSRF-TOKEN")
            },
            allow_redirects=True
        )

        token_response = self.session.post(
            url="/oauth2/token",
            data={
                "code": self.session.code,
                "redirect_uri": self.redirect_uri,
                "code_verifier": self.code_verifier,
                "grant_type": "authorization_code",
                "client_id": "client"
            }
        )

        self.token = token_response.json().get("access_token", None)
        return self.token
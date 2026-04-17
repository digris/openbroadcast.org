from social_core.utils import parse_qs
from social_core.backends.oauth import BaseOAuth2


class DeezerOAuth2(BaseOAuth2):
    """Deezer OAuth2 authentication backend"""

    name = "deezer"
    REDIRECT_STATE = False
    AUTHORIZATION_URL = "https://connect.deezer.com/oauth/auth.php"
    ACCESS_TOKEN_URL = "https://connect.deezer.com/oauth/access_token.php"
    ACCESS_TOKEN_METHOD = "GET"
    REVOKE_TOKEN_URL = "https://connect.deezer.com/oauth/revoke.php"
    REVOKE_TOKEN_METHOD = "GET"
    SCOPE_PARAMETER_NAME = "perms"
    SCOPE_SEPARATOR = ","
    DEFAULT_SCOPE = ["basic_access", "email"]
    EXTRA_DATA = [
        ("refresh_token", "refresh_token", True),
        ("expires_in", "expires"),
        ("token_type", "token_type", True),
    ]

    def get_user_details(self, response):
        """Return user details from Deezer account"""
        print("response", response)
        return {
            "email": response.get("email"),
            "username": response.get("name"),
        }

    def request_access_token(self, *args, **kwargs):

        kwargs["params"].update({"output": "json"})

        return self.get_json(*args, **kwargs)

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Deezer API"""

        return self.get_json(
            "https://api.deezer.com/user/me", params={"access_token": access_token,},
        )

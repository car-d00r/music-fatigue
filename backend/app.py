from litestar import Litestar, get, Request, Controller
from litestar.response import Redirect
from litestar.middleware.session import SessionMiddleware
from litestar.middleware.session.client_side import (
    ClientSideSessionBackend,
    CookieBackendConfig,
)
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
SCOPE = "user-library-read"
sp_oauth = SpotifyOAuth(
    client_id=os.environ["SPOTIPY_CLIENT_ID"],
    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
    scope="user-library-read",  # Adjust scope as needed
)
config = CookieBackendConfig(secret=os.environ["SECRET_KEY"].encode())


class SpotifyController(Controller):
    path = "/spotify"

    def before_request(request) -> None:
        # Get token from session
        token_info = request.session.get("spotify_token")

        if not token_info:
            raise Exception("Not authenticated")

        # Check if token needs refresh
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
            request.session["spotify_token"] = token_info

    def _get_client(self, request: Request) -> spotipy.Spotify:
        token_info = request.session.get("spotify_token")
        return spotipy.Spotify(auth=token_info["access_token"])

    @get("/user")
    async def get_user(self, request: Request) -> dict[str, str]:
        try:
            sp = self._get_client(request)
        except Exception as e:
            print(e)
        return {"user": sp.current_user()}


@get("/")
async def health_check() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return {"status": "Living the dream!"}


@get("/login")
async def spotify_login() -> dict[str, str]:
    auth_url = sp_oauth.get_authorize_url()
    return Redirect(auth_url)


@get("/callback")
async def set_initial_token(request: Request) -> dict[str, str]:
    code = request.query_params.get("code")
    token_info = sp_oauth.get_access_token(code)
    request.session["spotify_token"] = token_info
    return {"success": True, "message": "Authentication successful!"}


session_middleware = SessionMiddleware


def middleware_factory(app):
    return SessionMiddleware(app, ClientSideSessionBackend(config=config))


app = Litestar(
    route_handlers=[health_check, spotify_login, set_initial_token, SpotifyController],
    middleware=[middleware_factory],
)

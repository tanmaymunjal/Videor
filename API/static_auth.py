# inspired by https://github.com/tiangolo/fastapi/issues/858#issuecomment-876564020

from fastapi.staticfiles import StaticFiles
from API.api_auth import get_current_active_user


class AuthStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send) -> None:
        assert scope["type"] == "http"

        request = Request(scope, receive)
        await get_current_active_user(request)
        await super().__call__(scope, receive, send)

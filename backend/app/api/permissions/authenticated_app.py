from app.api.auth.auth import Auth
from app.models import App

from rest_framework import authentication


class IsAuthenticatedApp(authentication.BaseAuthentication):
    """Authenticate App Using Username And Password From Header

    Args:
        authentication (BaseAuthentication): Extending Base Class

    Raises:
        exceptions.AuthenticationFailed: Throws Username and Password Authentication Failure

    Returns:
        App: Request Authenticated App
    """

    def authenticate(self, request):
        auth = Auth(request, App)
        auth.authenticate()
        request.app = auth.app()
        return (auth.app(), None)

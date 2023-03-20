from rest_framework import generics

from rest_framework.throttling import UserRateThrottle
from app.api.auth.auth import Auth

from app.api.serializers.app_authenticate_serializer import AppAuthenticateSerializer
from app.models import App
from utils.api_response import ApiResponse
from utils.helpers import get_error_message


class AppAuthenticateView(generics.GenericAPIView):
    """ Returns app's payment credentials

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: App payment gateway's credentials
    """
    throttle_classes = [UserRateThrottle]
    serializer_class = AppAuthenticateSerializer

    def post(self, request):
        """Get Access Token For App Using Username And Password

        Args:
            request (request): django request

        Returns:
            list: list of serialized payment credentials
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.send_error(get_error_message(serializer), 400)

        auth = Auth(request, App)
        app = App.objects.filter(username=request.data['username']).first()

        if not app or not auth.match_password(request.data['password'], app.password):
            return ApiResponse.send_error('Username or Password Incorrect', 400)

        access_token = auth.generate_access_token(app, {})
        return ApiResponse.send_success(access_token)

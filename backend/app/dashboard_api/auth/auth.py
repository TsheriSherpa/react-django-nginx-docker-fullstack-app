import json
from datetime import datetime, timedelta

from rest_framework import exceptions

from utils.crypt_service import CryptService
from utils.helpers import dict_key_exists


class Auth:
    """ Authentication Class For Apps
        Current version only supports App model for authentication
    """

    request = None
    valid_minutes = 10
    decrypted_object = None
    authentication_class = None
    refresh_token_valid_minutes = 14400

    def __init__(self, request, authentication_class) -> None:
        self.request = request
        self.authentication_class = authentication_class

    def authenticate(self) -> None:
        """Authenticate app api request

        Raises:
            exceptions.AuthenticationFailed: exception on request not authenticated

        Returns:
            bool: returns True if authenticated else raises exceptions.AuthenticationFailed
        """
        auth_token = self.request.headers.get('Auth-Token')

        if auth_token is None:
            raise exceptions.AuthenticationFailed("Auth-Token Not Found")

        try:
            decrypted_string = CryptService.decrypt(auth_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed("Invalid Token Provided")

        self.decrypted_object = json.loads(decrypted_string)
        self.is_token_valid(self.decrypted_object)

    def get_body(self) -> dict:
        """Get body of decrypted token

        Raises:
            exceptions.AuthenticationFailed:  exception on request not authenticated

        Returns:
            dict: returns the decrypted body obtained from Auth-Token
        """
        if self.decrypted_object is None:
            raise exceptions.AuthenticationFailed(
                "Request is not authenticated")
        return self.decrypted_object

    def is_token_time_valid(self) -> bool:
        """Check if token time is valid

        Returns:
            bool: return False if expired else True
        """
        generated_at = self.get_body().get('generated_at')
        valid_minutes = self.get_body().get('valid_minutes')
        valid_time = datetime.strptime(
            generated_at, '%Y-%m-%d, %H:%M:%S') + timedelta(minutes=int(valid_minutes))

        if datetime.now() > valid_time:
            return False

        return True

    def is_token_valid(self, decrypted_object: dict) -> bool:
        """Check if the token is valid for given request

        Args:
            decrypted_object (dict): decrypted token dict object

        Raises:
            exceptions.AuthenticationFailed: raises on authentication failure

        Returns:
            bool: returns True if valid else False
        """
        requiredAuthKeys = [
            'app_id', 'username', 'message', 'valid_minutes', 'generated_at', 'type']

        for key in requiredAuthKeys:
            if not dict_key_exists(key, decrypted_object):
                raise exceptions.AuthenticationFailed("Invalid Auth Token")

        if not self.is_token_time_valid():
            raise exceptions.AuthenticationFailed("Token Expired")

        return True

    def app(self) -> object:
        """Returns the app associated with token

        Returns:
            Object: Authentication Class Object
        """
        id = self.get_body().get('app_id')
        return self.authentication_class.objects.filter(id=id).first()

    def match_password(self, txtPassword, encyrpted_password) -> bool:
        """Match plain text password against encrypted Password

        Args:
            txtPassword (str): plain text password
            encyrptedPassword (str): encrypted password
        Returns:
            match (bool) : True if matched else False
        """
        decrypted_password = CryptService.decrypt(encyrpted_password)
        if txtPassword == decrypted_password:
            return True
        return False

    def make_password(self, password) -> str:
        """Create Encrypted Password

        Args:
            password (str): plain text password

        Returns:
            encrypted_password (str): encrypted password
        """
        return CryptService.encrypt(password)

    def generate_access_token(self, app, message: dict, refresh_token=None) -> dict:
        """Generate access_token and refresh token for app

        Args:
            app (self.authenticated_class): Authentication Model Class

        Returns:
            dict: access_token and refresh_token dict
        """
        access_token_payload = self.make_token_payload(
            app, message)
        access_token = CryptService.encrypt(access_token_payload)

        refresh_token_payload = self.make_token_payload(
            app, message, access_token)

        if not refresh_token:
            refresh_token = CryptService.encrypt(refresh_token_payload)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def make_token_payload(self, app, message: dict, access_token=None) -> dict:
        """Generate body payload for token

        Args:
            app (App): App Model
            type (str): Either access_token or refresh_token
            message (dict): any message in dict format
            access_token (str): required incase of refresh_token generation

        Returns:
            dict: token body payload
        """
        return json.dumps({
            "app_id": app.id,
            "message": message,
            "username": app.username,
            "access_token": access_token if access_token else "",
            "type": "refresh_token" if access_token else "access_token",
            "generated_at": datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
            "valid_minutes": self.refresh_token_valid_minutes if access_token else self.valid_minutes
        })

    def app_from_refresh_token(self) -> authentication_class:
        try:
            decrypted_string = CryptService.decrypt(
                self.request.data['refresh_token'])
        except Exception:
            raise Exception("Invalid Refresh Token")

        self.decrypted_object = json.loads(decrypted_string)
        if self.decrypted_object['type'] != "refresh_token":
            raise Exception("Invalid Refresh Token")

        self.is_token_valid(self.decrypted_object)

        return self.authentication_class.objects.filter(id=self.decrypted_object['app_id']).first()

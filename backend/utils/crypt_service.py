from cryptography.fernet import Fernet
from django.conf import settings


class CryptService:
    """
        Cryptography Service Class
    """
    crypt = Fernet(settings.APP_API_SECRET)

    @ classmethod
    def encrypt(cls, message: str) -> str:
        """Encrypt the given string

        Args:
            message (str): string to be encrypted

        Returns:
            str: encrypted string
        """
        return cls.crypt.encrypt(message.encode()).decode("UTF-8")

    @ classmethod
    def decrypt(cls, encryptedString: str) -> str:
        """Decrypt the encrypted string

        Args:
            encryptedString (str): encrypted string

        Returns:
            str: decrypted string
        """
        return cls.crypt.decrypt(encryptedString.encode("UTF-8")).decode()

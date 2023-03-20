from django.db import models

from utils.crypt_service import CryptService


class App(models.Model):
    name = models.CharField(verbose_name="App Name", max_length=255)
    username = models.CharField(
        verbose_name="App Username", max_length=255, unique="true")
    password = models.CharField(verbose_name="App Password", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.password = CryptService.encrypt(self.password)
        return super(App, self).save(*args, **kwargs)

from django.db import models

# Create your models here.
class UserInfo(models.Model):
    email = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=5)
    phoneNum = models.CharField(max_length=13)

    def __str__(self):
        return self.name
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    email = models.CharField(max_length=100)
    nickname = models.CharField(max_length=12)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=5)
    phoneNum = models.CharField(max_length=13)

    def __str__(self):
        return self.name
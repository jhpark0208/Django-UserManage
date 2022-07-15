from rest_framework import serializers
from .models import UserInfo

class RegisterSerializer(serializers.ModelSerializer):
    class Meta :
        model = UserInfo
        fields = '__all__'
    
    def create(self, data):
        email = data.get('email')
        nickname = data.get('nickname')
        password = data.get('password')
        name = data.get('name')
        phoneNum = data.get('phoneNum')

        user = UserInfo(
            email = email,
            nickname = nickname,
            password = password,
            name = name,
            phoneNum = phoneNum
        )
        user.save()
        return user

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta :
        model = UserInfo
        fields = ['email', 'nickname', 'name', 'phoneNum']
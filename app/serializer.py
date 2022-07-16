from rest_framework import serializers
from .models import UserInfo
import bcrypt

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

        pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        pw = pw.decode('utf-8')

        user = UserInfo(
            email = email,
            nickname = nickname,
            password = pw,
            name = name,
            phoneNum = phoneNum
        )
        user.save()
        return user

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta :
        model = UserInfo
        fields = ['email', 'nickname', 'name', 'phoneNum']
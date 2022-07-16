from app.serializer import RegisterSerializer, UserInfoSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserInfo

# Default Python Module
import json, re, os, jwt, bcrypt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('JWT_ALGORITHM')

class VerifyView(APIView):
    def post(self, request):
        request = json.loads(request.body)

        p = re.compile('\d{6}')
        if p.match(request['pincode']) != None :
            token = jwt.encode(
                {
                    'exp':datetime.utcnow() + timedelta(minutes=10)
                },
                SECRET_KEY,
                ALGORITHM
            )
            return Response(
                {
                    "message" : "SMS 인증이 성공하였습니다.",
                    "token" : token
                }
                , status = status.HTTP_200_OK
            )
        else:
            return Response(
                    {
                        "message" : "6자리 숫자가 아닙니다."
                    }
                    , status = status.HTTP_400_BAD_REQUEST
                )        

class RegisterView(APIView):
    def post(self, request):
        Authorization = request.META.get('HTTP_AUTHORIZATION')
        try:
            jwt.decode(
                Authorization,
                SECRET_KEY,
                algorithms = ALGORITHM
            )

            request = json.loads(request.body)
            register_serializer = RegisterSerializer(data=request)
            if register_serializer.is_valid():
                register_serializer.save()
                return Response(
                    {
                        "message" : "회원가입이 되었습니다!"
                    }
                    , status = status.HTTP_200_OK
                )
            else:
                return Response(
                    register_serializer.errors
                    , status = status.HTTP_400_BAD_REQUEST
                )

        except jwt.ExpiredSignatureError:
            return Response(
                {
                    "message" : "Token Expired"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

class ResetView(APIView):
    def post(self, request):
        Authorization = request.META.get('HTTP_AUTHORIZATION')
        try:
            jwt.decode(
                Authorization,
                SECRET_KEY,
                algorithms = ALGORITHM
            )

            request = json.loads(request.body)
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if p.match(request["id"]) != None :
                UserInfo.objects.filter(email = request["id"]).update(password = request["pw"])
            else:
                UserInfo.objects.filter(nickname = request["id"]).update(password = request["pw"])

            return Response(
                {
                    "message" : "비밀번호가 재설정 되었습니다."
                },
                status = status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {
                    "message" : "Token Expired"
                },
                status = status.HTTP_400_BAD_REQUEST
            )        

class LoginView(APIView):
    def post(self, request):
        request = json.loads(request.body)
        p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if p.match(request["id"]) != None :
            user = UserInfo.objects.get(email = request["id"])
            if user is None:
                return Response(
                    {
                        "message": "존재하지않는 email 입니다."
                    },
                     status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if bcrypt.checkpw(request["pw"].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode(
                        {
                            'id': user.email,
                            'exp':datetime.utcnow() + timedelta(minutes=30)
                        },
                        SECRET_KEY,
                        ALGORITHM
                    )
                    return Response(
                        {
                            "message": "로그인에 성공하였습니다.",
                            "token" : token
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            "message": "비밀번호가 일치하지 않습니다."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            user = UserInfo.objects.get(nickname = request["id"])
            if user is None:
                return Response(
                    {
                        "message": "존재하지않는 nickname 입니다."
                    },
                     status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if bcrypt.checkpw(request["pw"].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode(
                        {
                            'id': user.nickname,
                            'exp':datetime.utcnow() + timedelta(minutes=30)
                        },
                        SECRET_KEY,
                        ALGORITHM
                    )
                    return Response(
                        {
                            "message": "로그인에 성공하였습니다.",
                            "token" : token
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            "message": "비밀번호가 일치하지 않습니다."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

class InfoView(APIView):
    def get(self, request):
        Authorization = request.META.get('HTTP_AUTHORIZATION')
        try:
            token = jwt.decode(
                Authorization,
                SECRET_KEY,
                algorithms = ALGORITHM
            )
            id = token.get('id')
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            
            user = None
            if p.match(id) != None:
                user = UserInfo.objects.get(email = id)
            else:
                user = UserInfo.objects.get(nickname = id)

            returnUser = UserInfoSerializer(user)
            return Response(
                returnUser.data,
                status = status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {
                    "message" : "Token Expired"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        
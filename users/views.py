from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
import jwt
import datetime
from .models import User
from django.contrib.auth.hashers import check_password


# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={
            "msg": "user created successfully, login to get the access token for further API calls"
        })


class LoginView(APIView):

    def get(self, request):

        try:
            record = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({
                "msg": "User does not exists or Invalid username ! try to register first"},
                status=status.HTTP_400_BAD_REQUEST)

        # print(make_password(request.data['password']))
        # if record.password == make_password(request.data['password']):
        if check_password(request.data['password'], record.password):

            payload = {
                'id': record.user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()

            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'access token': token
            }
            return response
        else:
            return Response(data={
                'msg': 'Invalid password'
            }, status=status.HTTP_400_BAD_REQUEST)

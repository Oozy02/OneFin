from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import jwt, datetime 

class Auth():
    def check_auth(self,req):
        """

        @rtype: object
        """
        token = req.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated !')
        try:
            payload = jwt.decode(token,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired !')
        return payload
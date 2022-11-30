from rest_framework.views import APIView
from OneFin.utils import Auth
from rest_framework.response import Response
from rest_framework import status
    
# Create your views here.


class RequestCounts(APIView):
    
    def get(self, request):
        
        Auth.check_auth(self, req=request)
        with open('api_logs.txt') as f:
            f = len(f.readlines())
    
        return Response(
            data={"count": f}
        )


class RequestCountsReset(APIView):

    def get(self, request):
        Auth.check_auth(self, req=request)
        open('api_logs.txt', 'w').close()
        
        return Response(
            data={"msg": "Counter reset successfully"}, status=status.HTTP_205_RESET_CONTENT)

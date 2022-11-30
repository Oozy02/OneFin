import yaml
import os
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from OneFin.utils import Auth


with open(os.path.dirname(os.path.abspath(__file__)) + '/config.yml') as f:
    
    data = yaml.load(f, Loader=yaml.FullLoader)


class AllMoviesView(APIView):
    def get(self, request):
        Auth.check_auth(self, req=request)
        
        url = 'https://demo.credy.in/api/v1/maya/movies/'+'?page='+str(request.data['page'])
        username = data['username']
        password = data['password']
        res = requests.get(url, auth=(username, password))
        while res.status_code == 500:
            res = requests.get(url, auth=(username, password))
            res.status_code = 200
        response = Response()

        response.data = res.json()
        return response

# Create your views here.

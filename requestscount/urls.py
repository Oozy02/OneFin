from django.urls import path, re_path
from .views import RequestCounts, RequestCountsReset


urlpatterns = [
     path('request-count', RequestCounts.as_view()),
     path('request-count/reset', RequestCountsReset.as_view())
]

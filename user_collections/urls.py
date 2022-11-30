from django.urls import path, re_path
from .views import Collections


urlpatterns = [
     path('collection', Collections.as_view()),
     re_path('collection/' + r'(?P<slug>[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})',
             Collections.as_view())
]

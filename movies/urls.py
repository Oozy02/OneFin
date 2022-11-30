from django.urls import path
from .views import AllMoviesView

urlpatterns = [
    path('movies', AllMoviesView.as_view())
]

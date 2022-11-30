from rest_framework.views import APIView
from .serializers import CollectionSerializer, MovieSerializer
from rest_framework.response import Response
from django.db.models import Count
from . import models
from django.db import transaction
from OneFin.utils import Auth
from rest_framework import status


# Create your views here.


class Collections(APIView):
    def post(self, request):

        payload = Auth.check_auth(self, req=request)

        with transaction.atomic():
            collection_raw_data = ['title', 'description']
            collection_data = self._get_required_data(collection_raw_data, request.data)
            collection_data['user_id'] = payload['id']

            serializer_collection = CollectionSerializer(data=collection_data)
            serializer_collection.is_valid(raise_exception=True)
            serializer_collection.save()

            temp = serializer_collection['collection_uuid'].value
            for i in range(len(request.data['movies'])):
                movies_data = request.data['movies'][i]
                movies_data['collection_uuid'] = temp
                serializer_movies = MovieSerializer(data=movies_data)
                serializer_movies.is_valid(raise_exception=True)
                serializer_movies.save()

        return Response(data={
            'Collection UUID': temp
        }, status=status.HTTP_201_CREATED)

    def get(self, request, **kwargs):

        payload = Auth.check_auth(self, req=request)

        if kwargs.items():
            try:
                collection = models.Collections.objects.get(user_id=payload['id'], collection_uuid=kwargs['slug'])

            except models.Collections.DoesNotExist:
                return Response({
                    "msg": "No collections match with the provided UUID."

                })
            collection = models.Collections.objects.filter(user_id=payload['id'], collection_uuid=kwargs['slug']) \
                .values()
            collection = list(collection)
            movies = list(models.Movies.objects.filter(collection_uuid=kwargs['slug']).values('title', 'description',
                                                                                              'genre', 'movie_uuid'))

            return Response(
                data={
                    "title": collection[0]['title'],
                    "description": collection[0]['description'],
                    "movies": movies
                },
                status=status.HTTP_200_OK
            )

        else:
            records = models.Collections.objects.filter(user_id=payload['id']).values().count()
            temp = []
            top = []
            for i in range(records):
                serialize = CollectionSerializer(models.Collections.objects.filter(user_id=payload['id']).values()[i])
                temp.append(serialize.data)
                temp[i].pop('user_id')
                top_genre = models.Movies.objects.filter(collection_uuid=temp[i]['collection_uuid']).values(
                    'genre').annotate(Count('genre'))
                top.append(list(top_genre))

            top_three_movies = self._get_top_movies(top=top)

            response = Response()
            response.data = {
                "is_success": True,
                "data": {
                    "Collection": temp,
                    "favourite_genres": top_three_movies
                }
            }
            response.status = status.HTTP_200_OK
            return response

    def put(self, request, slug):
        payload = Auth.check_auth(self, req=request)
        if slug:
            try:
                collection = models.Collections.objects.get(user_id=payload['id'], collection_uuid=slug)

            except models.Collections.DoesNotExist:
                return Response({
                    "msg": "No collections match with the provided UUID."
                })
            serializer_collection = CollectionSerializer(collection, data=request.data, partial=True)
            if serializer_collection.is_valid(raise_exception=True):
                serializer_collection.save()
            updated = []
            added_new = []
            if request.data['movies']:

                for j in range(len(request.data['movies'])):
                    # Checking if the movie already exists
                    try:
                        record = models.Movies.objects.get(collection_uuid=slug,
                                                           movie_uuid=request.data['movies'][j]['movie_uuid'])
                        serializer_movies = MovieSerializer(record, data=request.data['movies'][j], partial=True)
                        serializer_movies.is_valid(raise_exception=True)
                        serializer_movies.save()
                        updated.append(serializer_movies.data)
                    except models.Movies.DoesNotExist:
                        temp = slug
                        movies_data = request.data['movies'][j]
                        movies_data['collection_uuid'] = temp
                        serializer_movies = MovieSerializer(data=movies_data)
                        serializer_movies.is_valid(raise_exception=True)
                        serializer_movies.save()
                        added_new.append(serializer_movies.data)

            response = Response()
            response.data = {
                "title": serializer_collection.data['title'],
                "description": serializer_collection.data['description'],
                "movies": {
                    "added_new": added_new,
                    "updated": updated
                }
            }
            response.status = status.HTTP_201_CREATED
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        payload = Auth.check_auth(self, req=request)

        try:
            record = models.Collections.objects.get(user_id=payload['id'], collection_uuid=slug)
        except models.Collections.DoesNotExist:
            return Response({
                "msg": "No collections match with the provided UUID."
            })
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _get_required_data(keys: list, data: dict):
        result = {}
        for item in data.items():
            if item[0] in keys:
                result[item[0]] = str(item[1])
        return result

    @staticmethod
    def _get_top_movies(top):
        x = {}
        for i in range(len(top)):
            t = list(x.keys())
            for j in range(len(top[i])):
                if top[i][j]['genre'] in t:
                    x[top[i][j]['genre']] = x[top[i][j]['genre']] + top[i][j]['genre__count']
                else:
                    x[top[i][j]['genre']] = top[i][j]['genre__count']

        my_keys = sorted(x, key=x.get, reverse=True)[:3]
        return my_keys

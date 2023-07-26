from bson import ObjectId
from django.http import HttpResponse
from core.models import person_collection, marketplace_collection
from rest_framework import status, viewsets
import base64
from rest_framework.response import Response


def index(request):
    return HttpResponse("<h1>app is running</h1>")


def add_person(request):
    records = {
        "first_name": "Midhun",
        "last_name": "S"
    }
    person_collection.insert_one(records)
    return HttpResponse("New person added")

def get_all_person(request):
    persons = person_collection.find()
    return HttpResponse(persons)


class MarketplaceViewSet(viewsets.ViewSet):

    def destroy(self, request, pk=None):
        try:
            marketplace = marketplace_collection.find_one_and_delete({'_id': ObjectId(pk)})
            if marketplace:
                return Response("Marketplace deleted", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Marketplace not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error:", e)
            return Response("Error deleting Marketplace", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            marketplace = marketplace_collection.find_one({'_id': ObjectId(pk)}, {'_id': 0})
            if marketplace:
                return Response(marketplace, status=status.HTTP_200_OK)
            else:
                return Response("Marketplace not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error:", e)
            return Response("Error retrieving Marketplace", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            data = request.data
            marketplace = marketplace_collection.find_one_and_update(
                {'_id': ObjectId(pk)},
                {'$set': data},
                return_document=True
            )

            if marketplace:
                return Response(marketplace, status=status.HTTP_200_OK)
            else:
                return Response("Marketplace not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error:", e)
            return Response("Error updating Marketplace", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        all_marketplaces = list(marketplace_collection.find({}, {'_id': 0}))
        return Response(all_marketplaces)

    def create(self, request):
        try:
            name = request.data.get('name')
            logo = request.data.get('logo')

            if logo:
                logo_base64 = base64.b64encode(logo.read()).decode('utf-8')
            else:
                logo_base64 = None

            records = {
                "name": name,
                "logo": logo_base64
            }

            marketplace_collection.insert_one(records)
            return Response("Marketplace added", status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error:", e)
            return Response("Error adding Marketplace", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

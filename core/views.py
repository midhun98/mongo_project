from bson import ObjectId
from django.http import HttpResponse
from core.models import person_collection, marketplace_collection, brands_collection
from rest_framework import status, viewsets
from rest_framework.response import Response
import os
import uuid
from django.conf import settings


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

    def partial_update(self, request, pk=None):
        try:
            data = request.data
            logo_file = request.FILES.get('logo', None)

            # Handle logo file upload
            if logo_file:
                # Generate a unique file name and save the file to the server's media directory
                filename = f"{uuid.uuid4()}.png"
                file_path = os.path.join(settings.MEDIA_ROOT, 'marketplace_images', filename)

                # Save the image to the media directory
                with open(file_path, 'wb') as image_file:
                    image_file.write(logo_file.read())

                # Update the data dictionary with the new logo URL
                data['logo'] = os.path.join(settings.MEDIA_URL, 'marketplace_images', filename)

            # Perform the update on the database
            marketplace = marketplace_collection.find_one_and_update(
                {'_id': ObjectId(pk)},
                {'$set': data},
                return_document=True
            )

            if marketplace:
                return Response('Marketplace updated', status=status.HTTP_200_OK)
            else:
                return Response("Marketplace not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error:", e)
            return Response("Error updating Marketplace", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        all_marketplaces = list(marketplace_collection.find({}))
        for marketplace in all_marketplaces:
            marketplace['_id'] = str(marketplace['_id'])
        return Response(all_marketplaces)

    def create(self, request):
        try:
            name = request.data.get('name')
            logo = request.data.get('logo')

            if logo:
                # Generate a unique filename for the image
                filename = f"{uuid.uuid4()}.png"

                # Save the image to the media directory
                with open(os.path.join(settings.MEDIA_ROOT, 'marketplace_images', filename), 'wb') as image_file:
                    image_file.write(logo.read())

                # Save the image URL in the database
                records = {
                    "name": name,
                    "logo": os.path.join(settings.MEDIA_URL, 'marketplace_images', filename)
                }
            else:
                # If no logo is provided, save None in the database
                records = {
                    "name": name,
                    "logo": None
                }

            marketplace_collection.insert_one(records)
            return Response("Marketplace added", status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error:", e)
            return Response("Error adding Marketplace", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BrandsViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            name = request.data.get('name')
            logo = request.data.get('logo')
            marketplace = request.data.get('market')
            if logo:
                # Generate a unique filename for the image
                filename = f"{uuid.uuid4()}.png"

                # Save the image to the media directory
                with open(os.path.join(settings.MEDIA_ROOT, 'brands_images', filename), 'wb') as image_file:
                    image_file.write(logo.read())

                # Save the image URL in the database
                records = {
                    "name": name,
                    "logo": os.path.join(settings.MEDIA_URL, 'brands_images', filename),
                    "marketplace": marketplace
                }
            else:
                # If no logo is provided, save None in the database
                records = {
                    "name": name,
                    "logo": None,
                    "marketplace": marketplace
                }

            brands_collection.insert_one(records)
            return Response("Brand added", status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error:", e)
            return Response("Error adding Brand", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

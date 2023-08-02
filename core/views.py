from bson import ObjectId
from django.http import HttpResponse
from core.models import (users_collection,
                         marketplace_collection,
                         brands_collection)
from rest_framework import status, viewsets
from rest_framework.response import Response
import os
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from django.views import View


def index(request):
    desired_marketplace_id = ObjectId("64c228e8b14a7fcf0dcda36b")
    brands_in_desired_marketplace = brands_collection.find({
        "$or": [
            {"marketplace": str(desired_marketplace_id)},
            {"marketplace": {"$regex": f"{desired_marketplace_id}"}}
        ]
    })
    for brand in brands_in_desired_marketplace:
        print(brand)

    pipeline = [
        {
            "$group": {
                "_id": "$name",  # Group by the brand name
                "marketplace_count": {"$sum": 1}  # Count the number of occurrences for each brand name
            }
        }
    ]

    result = list(brands_collection.aggregate(pipeline))
    print(result)

    return HttpResponse("<h1>app is running</h1>")


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

    def list(self, request):
        all_brands = list(brands_collection.find({}))
        for brand in all_brands:
            brand['_id'] = str(brand['_id'])

            # Fetch the marketplace names if marketplaces exist
            marketplace_ids = brand.get('marketplace')
            if marketplace_ids:
                marketplace_ids = marketplace_ids.split(",")
                marketplace_names = []

                for marketplace_id in marketplace_ids:
                    marketplace = marketplace_collection.find_one({'_id': ObjectId(marketplace_id.strip())})
                    if marketplace:
                        marketplace_names.append(marketplace.get('name'))
                    else:
                        marketplace_names.append('Unknown Marketplace')

                brand['marketplace'] = marketplace_names
            else:
                brand['marketplace'] = 'No Marketplace Assigned'

        return Response(all_brands)

    def destroy(self, request, pk=None):
        try:
            brand = brands_collection.find_one_and_delete({'_id': ObjectId(pk)})
            if brand:
                return Response("brand deleted", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("brand not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error:", e)
            return Response("Error deleting brand", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            brand = brands_collection.find_one({'_id': ObjectId(pk)}, {'_id': 0})
            if brand:
                return Response(brand, status=status.HTTP_200_OK)
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
                file_path = os.path.join(settings.MEDIA_ROOT, 'brands_images', filename)

                # Save the image to the media directory
                with open(file_path, 'wb') as image_file:
                    image_file.write(logo_file.read())

                # Update the data dictionary with the new logo URL
                data['logo'] = os.path.join(settings.MEDIA_URL, 'brands_images', filename)

            # Perform the update on the database
            brand = brands_collection.find_one_and_update(
                {'_id': ObjectId(pk)},
                {'$set': data},
                return_document=True
            )

            if brand:
                return Response('Brand updated', status=status.HTTP_200_OK)
            else:
                return Response("Brand not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error:", e)
            return Response("Error updating Brand", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserVieswet(viewsets.ViewSet):
    def create(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            records = {
                "name": name,
                "email": email,
            }

            users_collection.insert_one(records)
            return Response("User added", status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error:", e)
            return Response("Error adding users", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        all_marketplaces = list(users_collection.find({}))
        for marketplace in all_marketplaces:
            marketplace['_id'] = str(marketplace['_id'])
        return Response(all_marketplaces)


class FireDetectionView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = load_model('trained_models/case_study2.h5')
        self.email_sent = False

    def preprocess_image(self, img):
        img = cv2.resize(img, (300, 300))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)
        return img

    def predict_fire(self, frame):
        x = self.preprocess_image(frame)
        classes = self.model.predict(x)
        if classes[0][0] < 0.5:
            result = "not fire"
        else:
            result = "fire"
            # Send an email when fire is detected
            if not self.email_sent:
                subject = "Fire Detected!"
                content = "A fire has been detected by the system."
                email = 'your_email@example.com'
                send_mail(subject, content, email, ['midhunskani@gmail.com'])
                self.email_sent = True
        return result

    def get(self, request):
        cap = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame from the webcam feed
            ret, frame = cap.read()

            # Perform fire detection on the frame
            result = self.predict_fire(frame)

            # Display the result on the frame
            cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if result == "not fire" else (0, 0, 255), 2)
            cv2.imshow('Fire Detection', frame)

            # Stop the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the webcam and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        return JsonResponse({"message": "Fire detection started!"})
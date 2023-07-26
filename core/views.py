from django.http import HttpResponse
from core.models import person_collection, marketplace_collection
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import base64

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
    persons =  person_collection.find()
    return HttpResponse(persons)


@csrf_exempt
@api_view(['POST'])
def create_marketplace_api(request):
    try:
        name = request.data['name']
        logo = request.data['logo']

        if logo:
            logo_base64 = base64.b64encode(logo.read()).decode('utf-8')
        else:
            logo_base64 = None

        records = {
            "name": name,
            "logo": logo_base64
        }

        marketplace_collection.insert_one(records)
        print("done")
        return HttpResponse("Marketplace added")
    except Exception as e:
        print("Error:", e)
        return HttpResponse("Error adding Marketplace", status=500)



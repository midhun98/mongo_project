from django.http import HttpResponse
from core.models import person_collection, marketplace_collection
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

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
    records = {
        "name": request.data['name'],
        "logo": request.data['logo']
    }
    marketplace_collection.insert_one(records)
    return HttpResponse("Marketplace added")


from django.shortcuts import render
from django.http import HttpResponse
from core.models import person_collection
# Create your views here.

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
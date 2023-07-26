from django.db import models
from db_connection import db
from mongoengine import Document, StringField, IntField, ImageField, DateTimeField, ReferenceField

# Create your models here.

person_collection = db['Person']
marketplace_collection = db['Marketplace']
class MarketPlace(Document):
    name = StringField(max_length=50)
    logo = ImageField(collection_name='market_place_images')


class ZipCode(Document):
    code = IntField()
    name = StringField(max_length=50)


class Brand(Document):
    name = StringField(max_length=50, null=True, blank=True)
    image = ImageField(collection_name='brand_images', null=True, blank=True)
    created_at = DateTimeField()
    market_place = ReferenceField(MarketPlace, null=True, blank=True)
    zip_code = ReferenceField(ZipCode, null=True, blank=True)


class Content(Document):
    name = StringField(max_length=100, null=True, blank=True)
    subject = StringField(max_length=1000, null=True, blank=True)
    image = ImageField(collection_name='images', null=True, blank=True)
    brands = ReferenceField(Brand, null=True, blank=True, reverse_delete_rule=4, dbref=False)
    marketplace = ReferenceField(MarketPlace, null=True, blank=True, reverse_delete_rule=4, dbref=False)

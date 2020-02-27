from rest_framework import serializers, exceptions
from .models import Location, Family, Product, Transaction, ProductInstance, Organization, OrganizationType

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location 
        fields = ('id','reference','title', 'description')

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family 
        fields = ('id', 'reference', 'title')

class ProductSerializer(serializers.ModelSerializer):
     class Meta:
        model = Product 
        fields = ('id','barcode', 'title', 'description','location', 'family','sku', 'refUsine')

class TransactionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction

    class Meta:
        model = Transaction 
        fields = ('sku', 'barcode','product', 'unitCost', 'quantity', 'reason', 'comment' )

class ProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstance
        fields = ('product','quantity','due_back','status')

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name','managed', 'contact','orga_type')

class OrganizationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationType
        fields = ('id','name')

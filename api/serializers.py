from rest_framework import serializers, exceptions
from .models import Location, Family, Product, Transaction

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location 
        fields = ('id','reference','title', 'description')

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family 
        fields = ('reference', 'title', 'description','unit','minQuantity')

class ProductSerializer(serializers.ModelSerializer):
     class Meta:
        model = Product 
        fields = ('id','sku','barcode', 'title', 'description','location', 'unitCost','family','quantity', 'minQuantity')

class TransactionSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction

    class Meta:
        model = Transaction 
        fields = ('sku', 'barcode','product', 'unitCost', 'quantity', 'reason', 'comment' )
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions
from .models import Location, Family, Product, Transaction, ProductInstance, Organization, Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id','firstname','lastname','username','email')

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class of the User Model

    The class member person is a nested representation
    """
    #person = PersonSerializer(many=True)
    externe = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'is_staff','externe')
        read_only_fields = ('username',)

    def get_externe(self, obj):
        try :
            if password in obj:
                return len(obj.password)==0
        except NameError:
            return 0
        else:
            return 0


 
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location 
        fields = ('id','reference','title', 'description')

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family 
        fields = ('id', 'reference', 'title')

class ProductSerializer(serializers.ModelSerializer):
    family = FamilySerializer(many=True, read_only=True)    
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
        fields = ('id', 'name','managed', 'contact', 'description')



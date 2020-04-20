from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions
from .models import Location, Family, Product, Transaction, ProductInstance, Entity, Profile, Affiliation
from rest_framework.serializers import ModelSerializer, IntegerField, RelatedField

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','firstname','lastname','username','email','acceptance')

class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class NewUserSerializer(serializers.Serializer):
    """
    Serializer for create new user endpoint.
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class of the User Model
    The class member person is a nested representation
    """
    profile = ProfileSerializer(many=False)
    externe = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'is_staff','profile','externe')
        read_only_fields = ('username',)

    def get_externe(self, obj):
        return len(obj.password)==0

class UserPublicSerializer(serializers.ModelSerializer):
    """
    Serializer class of the User Model
    The class member person is a nested representation
    """
    profile = ProfileSerializer(many=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name','profile')
        read_only_fields = ('username', 'email', 'first_name', 'last_name')

    def get_externe(self, obj):
        return len(obj.password)==0
 
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location 
        fields = ('id','reference','title', 'description')

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family 
        fields = ('id', 'reference', 'title')


class ProductSerializer(serializers.ModelSerializer):
    categories = FamilySerializer(many=True, read_only=True )
    class Meta:
        model = Product 
        fields = ('id','barcode', 'title', 'description','location', 'categories','sku', 'refUsine')
    

class ProductSetupSerializer(serializers.ModelSerializer):
    families = FamilySerializer(many=True, read_only=True )

    class Meta:
        model = Product 
        fields = ('id','barcode', 'title', 'description','location', 'families','sku', 'refUsine')
  

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

class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ['id', 'name', 'type']

class PublicAffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ['id', 'name', 'type']
        read_only_fields = ('id', 'name', 'type')

class EntitySerializer(serializers.ModelSerializer):
    managed = UserSerializer(many=True, read_only=True)
    affiliations = AffiliationSerializer(many=True, read_only=True)
    class Meta:
        model = Entity
        fields = ['id', 'name','managed', 'contact', 'affiliations', 'description']




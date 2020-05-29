from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
from .models import Entity, User, Affiliation, Tag, SpecificMaterial, SpecificMaterialInstance, GenericMaterial

from rest_framework.serializers import ModelSerializer, IntegerField, RelatedField

class AffiliationSerializer(serializers.ModelSerializer):
    """
    Serializer for Affiliation objects.
    """
    class Meta:
        model = Affiliation
        fields = ['id', 'name', 'type']

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
    externe = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'is_staff', 'rgpd_accept', 'affiliations', 'entities', 'externe')
        read_only_fields = ('username',)

    def get_externe(self, obj):
        return len(obj.password)==0

class UserPublicSerializer(serializers.ModelSerializer):
    """
    Public Serializer class for User objects
    Only visible to manager and only show username first_name and last_name and email
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('username', 'email', 'first_name', 'last_name')

    def get_externe(self, obj):
        return len(obj.password)==0

class EntitySerializer(serializers.ModelSerializer):
    """
    Serializer for Entity objects.
    """
    class Meta:
        model = Entity
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag objects.
    """
    class Meta:
        model = Tag
        fields = '__all__'

class GenericMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for generic material objects.
    """
    class Meta:
        model = GenericMaterial
        fields = '__all__'

class SpecificMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for specific material objects.
    """
    class Meta:
        model = SpecificMaterial
        fields = '__all__'

class SpecificMaterialInstanceSerializer(serializers.ModelSerializer):
    """
    Serializer for instance of specific material.
    """
    class Meta:
        model = SpecificMaterialInstance
        fields = '__all__'


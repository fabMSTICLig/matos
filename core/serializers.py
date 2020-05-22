from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
from .models import Entity, User, Affiliation, Tag, SpecificMaterial, SpecificMaterialInstance, GenericMaterial

from rest_framework.serializers import ModelSerializer, IntegerField, RelatedField

class AffiliationSerializer(serializers.ModelSerializer):
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
    Serializer class of the User Model
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('username', 'email', 'first_name', 'last_name')

    def get_externe(self, obj):
        return len(obj.password)==0

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class GenericMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericMaterial
        fields = '__all__'
        read_only_fields = ['entity']

class SpecificMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificMaterial
        fields = '__all__'
        read_only_fields = ['entity']

class SpecificMaterialInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificMaterialInstance
        fields = '__all__'
        read_only_fields = ['model']


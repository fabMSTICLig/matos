from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions
from .models import Entity, Profile, Affiliation
from rest_framework.serializers import ModelSerializer, IntegerField, RelatedField

class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ['id', 'name', 'type']
        
class ProfileSerializer(serializers.ModelSerializer):
    affiliations = AffiliationSerializer(many=True)
    acceptance = serializers.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ('id','email','acceptance','affiliations')

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




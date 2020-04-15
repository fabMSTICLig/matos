from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from api.models import Organization, Affiliation




class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class of the User Model

    The class member person is a nested representation
    """
    externe = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def get_externe(self, obj):
        try :
            if password in obj:
                return len(obj.password)==0
        except NameError:
            return 0
        else:
            return 0

    def update(self, instance, validated_data):
        """
        Overload the update method for updating the nested person 
        """
     
        user = None
        print("Update user serial")
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            # A non admin user cannot change is supervisor and charter member
            if(user.is_staff == False):
                    raise exceptions.PermissionDenied(
                        detail="You are not allowed to change this field")
            instance.username = validated_data.get('username', instance.username) 
            print(instance.username)  
            instance.save()
           # this will not throw an exception,
        # as `profile` is not part of `validated_data`
        return super(UserSerializer, self).update(instance, validated_data)


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name',)
        read_only_fields = ('username', 'first_name', 'last_name',)


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


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ['id', 'name', 'type']

class OrganizationSerializer(serializers.ModelSerializer):
    managed = UserSerializer(many=True)
    affiliations = AffiliationSerializer(many=True, read_only=True)
    class Meta:
        model = Organization
        fields = ['id', 'name','managed', 'contact', 'affiliations', 'description']

 
class OrganizationPublicSerializer(OrganizationSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']
        readonly = ['id', 'name']




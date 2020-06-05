from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
from rest_framework.utils import model_meta
from .models import Entity, User, Affiliation, Tag, SpecificMaterial, SpecificMaterialInstance, GenericMaterial, Loan, LoanGenericItem

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

class GenericMaterialPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for generic material objects.
    """
    class Meta:
        model = GenericMaterial
        exclude = ['localisation']

class SpecificMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for specific material objects.
    """
    class Meta:
        model = SpecificMaterial
        fields = '__all__'

class SpecificMaterialPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for specific material objects.
    """
    class Meta:
        model = SpecificMaterial
        exclude = ['localisation']

class SpecificMaterialInstanceSerializer(serializers.ModelSerializer):
    """
    Serializer for instance of specific material.
    """
    class Meta:
        model = SpecificMaterialInstance
        fields = '__all__'


class LoanGenericItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanGenericItem
        fields = ('material','quantity')

class LoanSerializer(serializers.ModelSerializer):
    generic_materials = LoanGenericItemSerializer(source="loangenericitem_set",many=True)
    class Meta:
        model = Loan
        #fields = ('id', 'status', 'checkout_date', 'user', 'entity', 'due_date', 'return_date', 'parent', 'specific_materials', 'comments', 'generic_materials')
        fields = '__all__'
    def create(self, validated_data):
        # Create the book instance
        specmats=validated_data.pop('specific_materials')
        genmats=validated_data.pop('loangenericitem_set')
        loan = Loan.objects.create(**validated_data)
        for mat in specmats:
            loan.specific_materials.add(mat)
        loan.save()
        # Create or update each page instance
        for item in genmats:
            item = LoanGenericItem(quantity=item['quantity'],material=item['material'], loan=loan)
            item.save()

        return loan

    def update(self, instance, validated_data):
        loangen = validated_data.pop('loangenericitem_set')
        info = model_meta.get_field_info(instance)
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        # Delete any pages not included in the request
        item_ids = [item['material'].id for item in loangen]
        for item in instance.loangenericitem_set.all():
            if item.material.id not in item_ids:
                item.delete()

        # Create or update page instances that are in the request
        for item in loangen:
            loan_item, created = LoanGenericItem.objects.get_or_create(material=item['material'], loan=instance)
            loan_item.quantity = item['quantity']
            loan_item.save()

        return instance

    def validate(self, data):
        if(data['checkout_date'] > data['due_date']):
            raise serializers.ValidationError("La date de rendu doit être après la date de sortie")
        if(data['return_date'] and data['checkout_date'] > data['return_date']):
            raise serializers.ValidationError("La date de retour doit être après la date de sortie")
        entity = data['entity']
        for mat in data['specific_materials']:
            if mat.model.entity != entity:
                raise serializers.ValidationError("Tout les matériels doivent apartenir à l'entité preteuse.")
        for item in data['loangenericitem_set']:
            if item['material'].entity != entity:
                raise serializers.ValidationError("Tout les matériels doivent apartenir à l'entité preteuse.")
        return data

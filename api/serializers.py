from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions
from .models import Location, Family, Product, Transaction, ProductInstance, Organization, Person
from rest_framework.serializers import ModelSerializer, IntegerField, RelatedField

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

class FamilyRelatedField(RelatedField):
    def get_queryset(self):
        return Family.objects.all()

    def to_representation(self, instance):
        return {'reference': instance.reference, 'title': instance.title, 'material': instance.material.title}

    def to_internal_value(self, data):
        title = data.get('title', None)
        reference = data.get('reference', None) 
        material = data.get('material', None)
        try:
            product = Product.objects.get(title=material)
        except Setting.DoesNotExist:
            raise serializers.ValidationError('bad inventor')
        return Family(title=title, reference=reference, material=product)


class ProductSerializer(serializers.ModelSerializer):
    categories = FamilyRelatedField(many=True )
    class Meta:
        model = Product 
        fields = ('id','barcode', 'title', 'description','location', 'categories','sku', 'refUsine')
    
    depth = 1
    def update(self, instance, validated_data):
            families_data = validated_data.pop('families')
            # Unless the application properly enforces that this field is
            # always set, the following could raise a `DoesNotExist`, which
            # would need to be handled.

            instance.barcode = validated_data.get('barcode', instance.barcode)
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.location = validated_data.get('location', instance.location)
            instance.sku = validated_data.get('sku', instance.sku)
            instance.refUsine = validated_data.get('refUsine', instance.refUsine)
            for family in families_data:
                print(family)
                family = Family.objects.get(pk=family_id)
                instance.set(family)
            #families = Family.objects.filter(product__in=families_data)
            print(instance)
            # instance.families.set(families)
            #families.save()
            return instance    

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



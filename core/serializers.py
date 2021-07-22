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
        #remove if not using ldap info update : 'email', 'first_name', 'last_name'
        read_only_fields = ('username','email', 'first_name', 'last_name')

    def get_externe(self, obj):
        return len(obj.password)==0


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Public Serializer class for User objects
    Only visible to manager and only show username first_name and last_name and email
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'affiliations')
        read_only_fields = ('username', 'email', 'first_name', 'last_name', 'affiliations')

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
    Serializer for Generic Material objects.
    """
    class Meta:
        model = GenericMaterial
        fields = '__all__'

class GenericMaterialPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for Generic Material objects.
    """
    class Meta:
        model = GenericMaterial
        exclude = ['localisation', 'active']

class SpecificMaterialPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for Specific Material objects.
    """
    class Meta:
        model = SpecificMaterial
        fields = ['id','name','ref_int', 'ref_man', 'description', 'tags', 'entity', 'instances']

class SpecificMaterialInstanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Instance of Specific Material.
    """
    class Meta:
        model = SpecificMaterialInstance
        fields = '__all__'

class SpecificMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for Specific Material objects.
    """
    instances = SpecificMaterialInstanceSerializer(many=True, read_only=True)
    class Meta:
        model = SpecificMaterial
        fields = ['id','name','ref_int', 'ref_man', 'description', 'tags', 'entity', 'instances', 'localisation', 'active']

class SpecificMaterialUserSerializer(serializers.ModelSerializer):
    """
    Serializer for specific material objects.
    """
    class Meta:
        model = SpecificMaterial
        fields = ['id','name','description']

class LoanGenericItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Loan generic items related
    """
    quantity = serializers.IntegerField(min_value=1, max_value=10000)
    class Meta:
        model = LoanGenericItem
        fields = ('material','quantity')

class LoanSerializer(serializers.ModelSerializer):
    """
    Serializer for Loan objects
    """
    generic_materials = LoanGenericItemSerializer(source="loangenericitem_set",many=True)
    models = serializers.SerializerMethodField()

    def get_models(self, obj):
        models=set()
        if hasattr(obj, 'specific_materials'):
            for item in obj.specific_materials.all():
                if(item.model.entity_id == obj.entity.id):
                    models.add(item.model.id)
        return list(models)

    class Meta:
        model = Loan
        fields = ('id', 'status', 'checkout_date', 'user', 'entity', 'due_date', 'return_date', 'comments', 'specific_materials', 'models', 'generic_materials', 'parent', 'child')
        read_only_fields=('child', 'models')
        extra_kwargs={'status':{'error_messages':{'invalid_choice':'Veuillez séléctionner un status pour le prêt'}}}

    def create(self, validated_data):
        """
        Create Loan object with Specific Materials and Loan Generic Item objects related and
        return Loan
        """
        # Create Loan object and set materials
        specmats=validated_data.pop('specific_materials')
        genmats=validated_data.pop('loangenericitem_set')
        loan = Loan.objects.create(**validated_data)
        for mat in specmats:
            loan.specific_materials.add(mat)
        loan.save()
        # Create Loan Generic Item
        for item in genmats:
            item = LoanGenericItem(quantity=item['quantity'],material=item['material'], loan=loan)
            item.save()

        return loan

    def update(self, instance, validated_data):
        """
        Update Loan with Specific Materials and Generic Materials relation and new value attributes
        """
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

        # Delete any Material Generic not included in the request
        item_ids = [item['material'].id for item in loangen]
        for item in instance.loangenericitem_set.all():
            if item.material.id not in item_ids:
                item.delete()

        # Save quantity of Material Generic in validated data
        for item in loangen:
            loan_item, created = LoanGenericItem.objects.get_or_create(material=item['material'], loan=instance)
            loan_item.quantity = item['quantity']
            loan_item.save()

        return instance


    def validate(self, data):
        """
        Validate Loan
        Check checkout_date and return_date and specific_materials error
        Check Material Generic and Specific Material are included in Entity Loan
        Check if Specific Material is not interfering with Specific Material in a current Loan, a next Loan or an ended Loan
        """
        if('parent' in data and data['parent'] is not None):
            loan_parent = Loan.objects.get(id=data['parent'].id)
            if(data['checkout_date'] < loan_parent.checkout_date):
                raise serializers.ValidationError("La date de sortie doit être postérieure à celle du prêt parent " + str(loan_parent.checkout_date))
        if(data['checkout_date'] > data['due_date']):
            raise serializers.ValidationError("La date de rendu doit être après la date de sortie")
        #Si la date de retour est défini
        if(data['return_date'] and data['checkout_date'] > data['return_date']):
            raise serializers.ValidationError("La date de retour doit être après la date de sortie")
        if(len(data['specific_materials']) == 0 and len(data['loangenericitem_set']) == 0):
            raise serializers.ValidationError("Un prêt doit contenir au moins un matériel.")
        entity = data['entity']
        for mat in data['specific_materials']:
            if mat.model.entity != entity:
                raise serializers.ValidationError("Tout les matériels doivent apartenir à l'entité preteuse.")
        for item in data['loangenericitem_set']:
            if item['material'].entity != entity:
                raise serializers.ValidationError("Tout les matériels doivent apartenir à l'entité prêteuse.")
        # SPEC MAT
        #conflit prêts en cours
        loans = Loan.objects.filter(specific_materials__in=data['specific_materials'], status=Loan.Status.ACCEPTED, checkout_date__lte=data['checkout_date'], return_date=None, due_date__gt=data['checkout_date']).distinct()
        if('id' in self.initial_data):
            loans = loans.exclude(id=self.initial_data['id'])
        for loan in loans:
            materialintersec = [ x.name for x in loan.specific_materials.all() if x in data['specific_materials']]
            raise serializers.ValidationError("Prêt en cours pour le matériel suivant : "+str(materialintersec[0])+" - jusqu'au "+str(loan.due_date))
        #conflit prêts en fini
        loans = Loan.objects.filter(specific_materials__in=data['specific_materials'], status=Loan.Status.ACCEPTED, checkout_date__lte=data['checkout_date'], return_date__gt=data['checkout_date'])
        if('id' in self.initial_data):
            loans = loans.exclude(id=self.initial_data['id'])
        for loan in loans:
            materialintersec = [ x.name for x in loan.specific_materials.all() if x in data['specific_materials']]
            raise serializers.ValidationError("Prêt en cours pour le matériel suivant : "+str(materialintersec[0])+" - jusqu'au "+str(loan.return_date))
        #conflit prêts dans le future
        loans = Loan.objects.filter(specific_materials__in=data['specific_materials'], status=Loan.Status.ACCEPTED, checkout_date__gte=data['checkout_date'])
        if('id' in self.initial_data):
            loans = loans.exclude(id=self.initial_data['id'])
        for loan in loans:
            if data['return_date']:
                if data['return_date'] > loan.checkout_date:
                    materialintersec = [ x.name for x in loan.specific_materials.all() if x in data['specific_materials']]
                    raise serializers.ValidationError("Le matériel "+str(materialintersec[0])+" doit être retourné avant le "+str(loan.checkout_date))
            elif data['due_date']> loan.checkout_date:
                materialintersec = [ x.name for x in loan.specific_materials.all() if x in data['specific_materials']]
                raise serializers.ValidationError("Le matériel "+str(materialintersec[0])+" doit être rendu avant le "+str(loan.checkout_date))
        #GEN MAT
        for item in data['loangenericitem_set']:
            if(item['material'].quantity == 0):
                continue
            if(item['material'].quantity < item['quantity']):
                raise serializers.ValidationError("Pas assez de "+item['material'].name+" en stock "+str(item['material'].quantity)+" max")
            loanslist = []
            structlist=[]
            #Creation d'une structure contenant l'ensemble des prêts checvauchant le prêt courant
            #conflit prêt en cours
            loans = Loan.objects.filter(generic_materials__id=item['material'].id, status=Loan.Status.ACCEPTED, checkout_date__lte=data['checkout_date'], return_date=None, due_date__gt=data['checkout_date']).distinct()
            if('id' in self.initial_data):
                loans = loans.exclude(id=self.initial_data['id'])
            loanslist.extend(loans)
            #conflit prêts en fini
            loans = Loan.objects.filter(generic_materials__id=item['material'].id, status=Loan.Status.ACCEPTED, checkout_date__lte=data['checkout_date'], return_date__gt=data['checkout_date'])
            if('id' in self.initial_data):
                loans = loans.exclude(id=self.initial_data['id'])
            loanslist.extend(loans)
            #conflit prêts dans le future
            if data['return_date']:
                loans = Loan.objects.filter(generic_materials__id=item['material'].id, status=Loan.Status.ACCEPTED, checkout_date__range=(data['checkout_date'], data['return_date'])).distinct()
            else:
                loans = Loan.objects.filter(generic_materials__id=item['material'].id, status=Loan.Status.ACCEPTED, checkout_date__range=(data['checkout_date'], data['due_date'])).distinct()
            if('id' in self.initial_data):
                loans = loans.exclude(id=self.initial_data['id'])
            loanslist.extend(loans)
            for loan in loanslist:
                quantity = loan.loangenericitem_set.get(material=item['material']).quantity
                struct = {'id':loan.id, 'quantity': quantity, 'checkout_date': loan.checkout_date, 'end_date': loan.return_date if loan.return_date else loan.due_date }
                structlist.append(struct)
            structlist.append({'id':-1, 'quantity': item['quantity'], 'checkout_date': data['checkout_date'], 'end_date': data['return_date'] if data['return_date'] else data['due_date'] })
            #liste ordonnée par date de sortie
            structlist.sort(key=lambda x:x['checkout_date']) 
            lenlist = len(structlist)
            i = 0
            index=-1
            maxtot=0
            while i<lenlist:
                if index==-1 and structlist[i]['id']==-1:
                    index=i
                #on commence que quand on est tombé sur le prêt courant
                if index != -1:
                    y = 0
                    total = structlist[i]['quantity']
                    while y < lenlist:
                        if i!=y and  structlist[i]['checkout_date'] >= structlist[y]['checkout_date'] and structlist[i]['checkout_date'] < structlist[y]['end_date']:
                            total = total + structlist[y]['quantity']
                        y = y+1
                    if(total > item['material'].quantity):
                        maxtot = maxtot if total-item['material'].quantity <= maxtot else total-item['material'].quantity
                i = i+1
            if(maxtot > 0):
                raise serializers.ValidationError("Pas assez de quantité en stock pour "+item['material'].name+" ( "+str(maxtot)+" manquant(s) ) pour les dates selectionnées" )

        return data

class LoanNestedSerializer(serializers.ModelSerializer):
    """
    Serializer to get Loan nested User
    """
    specific_materials = SpecificMaterialUserSerializer(many=True, read_only=True)
    generic_materials = GenericMaterialSerializer(many=True, read_only=True)
    class Meta:
        model = Loan
        fields = ('id','status', 'checkout_date', 'user', 'entity', 'due_date', 'return_date', 'comments','specific_materials', 'generic_materials', 'parent', 'child')


class EntityNestedSerializer(serializers.ModelSerializer):
    """
    Serializer for Nested Entity objects.
    """
    class Meta:
        model = Entity
        fields = ('name','description','contact')

class UserDataSerializer(serializers.ModelSerializer):
    """
    Serializer class of the User Model
    The class member person is a nested representation
    """
    externe = serializers.SerializerMethodField()
    entities = EntityNestedSerializer(many=True, read_only=True)
    loans = LoanNestedSerializer(many=True, read_only=True)
    affiliations = AffiliationSerializer(many=True, read_only=True)
    class Meta:
        model = get_user_model()
        fields = ('rgpd_accept', 'affiliations', 'entities', 'externe','loans')
        read_only_fields = ('rgpd_accept','affiliations','entities','externe')

    def get_externe(self, obj):
        return len(obj.password)==0

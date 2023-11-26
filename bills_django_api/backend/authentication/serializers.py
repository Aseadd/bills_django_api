from rest_framework import serializers
from .models import User, Bill, Payment, Report, Reminder, Customer, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
# class BillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bill
#         fields = ['id', 'bill_name', 'bill_amount', 'bill_date', 'status', 'biller_name']
#     def create(self, validated_data):
#         user = self.context["request"].user
#         bill = Bill.objects.create(user=user, **validated_data)
#         return bill
        
class BillSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Bill
        fields = ['id', 'bill_name', 'bill_amount', 'bill_date', 'status', 'biller_name']
        read_only_fields = ['id']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'password']
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
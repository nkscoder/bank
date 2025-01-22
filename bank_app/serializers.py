from rest_framework import serializers
from .models import Account
from django.contrib.auth.models import User 

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    balance = serializers.DecimalField(max_digits=10, decimal_places=2) 
    class Meta:
        model = Account
        fields = ['user', 'account_number', 'pin', 'balance']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['balance'] = str(representation['balance'])  
        return representation    
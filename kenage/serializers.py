from .models import User, Products
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','phone_number', 'country','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # print("serializer data ====>", validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
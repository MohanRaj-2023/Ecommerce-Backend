from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class ProductVariantSerializer(serializers.ModelSerializer):
        color = serializers.SerializerMethodField()
        size = serializers.SerializerMethodField()
        class Meta:
            model = ProductVariant
            fields = ["size","color","stockcount"]
        
        def get_size(self,obj):
            return obj.size.name if obj.size else None
        
        def get_color(self,obj):
            return obj.color.name if obj.color else None

class ProductsSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(many=True,read_only=True)

    class Meta:
       model = Products
       fields = ["id","category","productname","image","vendor",
                 "productinfo","rating","orginal_price","selling_price",
                 "status","trending","created_at","gender","variant"]
       
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['username','first_name','last_name','email','password']

class CustomTokenObtainSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['username','email','is_active']
        
    def get_token(self,user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
       model = Category
       fields = "__all__"

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
#from .Products import products
from django.http import JsonResponse
from .serializer import *
from .models import Products
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# To generate Tokens
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

#To send email and generate token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View

from django.template import TemplateSyntaxError

#To filter the data based on search
from rest_framework import filters
from django.db.models import Min, Max

#To increase the speed of signup
import threading

# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)
    
    def run(self):
        self.email_message.send()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
   @classmethod
   def get_token(cls,user): #add data to JWT.io
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
         
        return token
    
   def validate(self,attrs): #add data along with Api token
        data = super().validate(attrs)
        #user = self.user
        serializer = CustomTokenObtainSerializer(self.user).data
        for key,value in serializer.items():
            data[key]=value

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class UserDetailsView(APIView):
        
    def get(self,request):
        permission_class = [IsAuthenticated]
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
        

    

class Products_Api(APIView):
     def get(self,request):
        products = Products.objects.all()
        print('product:................',products)
        serializer = ProductsSerializer(products,many=True)
        return Response(serializer.data)

class GetProduct(APIView):
    def get(self,request,pk):
        product = Products.objects.get(id=pk)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)

class UserSignupView(APIView):
    def post(self,request):
        try:
             data = request.data
             user = User.objects.create(username=data['email'],first_name=data['fname'],last_name=data['lname'],email=data['email'],
             password=make_password(data['password']),is_active=False)
                  
             #Generate token for send mail
             email_subject = 'Activate Account'
             message = render_to_string(
                "activate.html",
                {
                    'user':user,
                    'domain':'https://ecommerce-backend-szaj.onrender.com',
                    'user_id':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':generate_token.make_token(user)
                }
             )
             print('MESSAGE:',message)
             email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[data['email']])
             EmailThread(email_message).run()
            #  serializer = UserSerializer(user) 
            #  return Response(serializer.data)
            
             return Response({"details": "Check your mail to activate  your account"})
        
        except Exception as error:
            return Response({"details": "User with the email is already exist"})



class ActivateaccountView(APIView):
    def get(self,request,uidb64,token):
        try:
            print("UIDB:",uidb64)
            uid = force_text(urlsafe_base64_decode(uidb64))
            print("UID_DECODED:",uid)
            user = User.objects.get(pk=uid)
        except :
            user=None

        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            return render(request,'activate_success.html')
        else:
            return render(request,'activate_fail.html')
        

class CategorieViews(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategoriesSerializer(categories,many=True)
        return Response(serializer.data)



class CategorieProductsView(APIView):
    def get(self,request,categoriename):
        products = Products.objects.filter(category__name=categoriename)
        serializer = ProductsSerializer(products,many=True)
        print("Variants:",serializer.data)
        return Response(serializer.data)
    
class Searchfilter(ListAPIView):
        queryset = Products.objects.all()
        serializer_class = ProductsSerializer
        filter_backends = [filters.SearchFilter,
                           filters.OrderingFilter]
        search_fields = ["productname","productinfo","category__name"]
        ordering_fields = ["productname","selling_price","rating"]

        
        # def list(self,request,*args,**kargs):
        #     response = super().list(request,*args,**kargs)
        
        #     price_range = Products.objects.aggregate(Min_price = Min("selling_price"),Max_price = Max("selling_price"))

        #     response.data={
        #         "min_price": price_range["Min_price"],
        #         "max_price": price_range["Max_price"],
        #         "products" : response.data
        #     }
            
        # return Response(response.data)

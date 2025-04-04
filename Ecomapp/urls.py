from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('',UserDetailsView.as_view(),name='home'),
    path('products/',Products_Api.as_view(),name='products'),
    path('product/<str:pk>/',GetProduct.as_view(),name='getproduct'),
    path('user/signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/signup/',UserSignupView.as_view(),name='signup'),
    path('activate/<uidb64>/<token>/',ActivateaccountView.as_view(),name='activate'),
    path('categories/',CategorieViews.as_view(),name="categories"),
    path('categorie/<str:categoriename>/',CategorieProductsView.as_view(),name="categorieproducts"),
    path('product/',Searchfilter.as_view(),name="search"),
]


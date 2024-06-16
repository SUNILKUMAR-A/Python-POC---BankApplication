from django.urls import path
from CustomerApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('signup/',views.signupApi),
    path('login/',views.loginApi),
    path('transaction/',views.transactionApi),
    path('getbalance/',views.balanceApi)

]
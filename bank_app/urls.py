from django.urls import path
from .views import *

urlpatterns = [
    path('create_account/', create_account, name='create_account'),
    path('login/', login, name='login'),
    path('account/details/', get_account_details, name='account-details'),
]

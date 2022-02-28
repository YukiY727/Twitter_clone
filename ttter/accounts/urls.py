
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('create_data_input/', views.UserDataInput.as_view(), name="create_data_input"),
    path('create_confirm/', views.UserDataConfirm.as_view(), name="create_confirm"),
    path('create_user/', views.UserDataCreate.as_view(), name='create_user'),
]

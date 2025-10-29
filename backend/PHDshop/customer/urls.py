from django.urls import path
from . import views
from .views import AddressList, AddressDetail


urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('register', views.CreateUserView.as_view(), name='create_user'),
    path('update/', views.UpdateUserView.as_view(), name='update_user'),
    path('login/', views.LoginView.as_view(), name='login_user'),

    path('<str:username>/submit-score/', views.submit_score, name='submit_score'),


    path('addresses/', AddressList.as_view(), name='address-list'),  # List and create addresses
    path('addresses/<int:id>/', AddressDetail.as_view(), name='address-detail'),  # Retrieve, update, and delete an address
]


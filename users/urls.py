from django.urls import path
from . import views

urlpatterns = [    
    path('login/', views.my_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.my_logout, name='logout'),
    path('<int:pk>/', views.profile, name='profile'),
]
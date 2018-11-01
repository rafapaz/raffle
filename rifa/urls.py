from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rifa/new/', views.raffle_new, name='raffle_new'),
    path('rifa/edit/<int:pk>/', views.raffle_edit, name='raffle_edit'),
    path('rifa/<int:pk>/', views.raffle_detail, name='raffle_detail'),
    path('rifa/choose/<int:pk>/<int:num>', views.choose, name='choose'),
]

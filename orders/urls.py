from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('history/', views.order_list_view, name='order_list'),
    path('history/<int:order_id>/', views.order_detail_view, name='order_detail'),
]
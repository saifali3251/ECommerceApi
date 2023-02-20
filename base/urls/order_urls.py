from django.urls import path
from base.views import order_views as views
# from rest_framework_simplejwt.views import TokenObtainPairView
from base.views.user_views import MyTokenObtainPairSerializer, MyTokenObtainPairView


urlpatterns = [
  path('add/',views.addOrderItems,name='orders-add'),
  path('',views.getOrders,name='getorders'),
  path('myorders/',views.getMyOrders,name='my-orders'),

  path('<str:pk>/deliver/',views.updateOrderToDelivered,name='order-deliver'),
  path('<str:pk>/',views.getOrderById,name='order-by-id'),
  path('<str:pk>/pay',views.updateOrderToPaid,name='paid'),
]

import imp
from django.urls import path
from base.views import product_views as views

# the order of path is important. We put create/ about <str:pk> so that the create may not be treated as pk for getProduct
urlpatterns = [

    path('',views.getProducts,name='getProducts'),
    path('create/',views.createProduct,name='createProduct'),
    path('upload/',views.uploadImage,name='uploadImage'),
    path('<str:pk>/reviews/',views.createProductReview,name='product-review'),
    path('<str:pk>',views.getProduct,name='getProduct'),
    path('update/<str:pk>',views.updateProduct,name='updateProduct'),
    path('delete/<str:pk>',views.deleteProduct,name='deleteProduct'),
]

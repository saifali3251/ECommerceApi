from django.urls import path
from base.views import user_views as views
# from rest_framework_simplejwt.views import TokenObtainPairView
from base.views.user_views import MyTokenObtainPairSerializer, MyTokenObtainPairView


urlpatterns = [
    # path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('login/',views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    # will give us userProfile
    path('profile/',views.getUserProfile,name='user-profile'),
    path('profile/update/',views.updateUserProfile,name='update-profile'),
    path('',views.getUsers,name='users'),
    path('delete/<str:pk>/',views.deleteUsers,name='delete-users'),
    path('register/',views.registerUser,name='register'),
    path('update/<str:pk>/',views.updateUser,name='update-user'),
    # below route should be at last to avoid conflict with other routes
    path('<str:pk>/',views.getUserById,name='get-user'),
]

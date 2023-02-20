from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from base.serializers import UserSerializer,UserSerializerWithToken
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status

# Create your views here.
# these two classes are copied from customizing_claims_token from drf official website
# what these classed will do is, by default when someone logs in, only access token and refresh tokens are generated
# we want to generate few more values like username and email. So we have customized this predefined validate function of this
# TokenObtainPairSerializer class and added those username and email fields into it.
# So now if someone logs in, we will get the username and emails also
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # This method will return username and email along with access and refresh token so it can be used in frontend
    def validate(self,attrs):
      data = super().validate(attrs) #this line ensures that we already getting refresh token and access token since we are inheriting thsi method from its parent

      serializer = UserSerializerWithToken(self.user).data
      # Here we are outputting all the fiedls we added in UserSerializer 
      for k,v in serializer.items():
        data[k] = v
      return data


'''
      # Instead of using multiple lines we loop and store data
      # data['username'] = self.user.username
      # data['email'] = self.user.email
      # data['password '] = self.user.password


    # this belowe method will return a JWT which will contain username and email token
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #     # Add custom claims
    #     token['username'] = user.username
    #     token['message'] = 'hello world'
    #     return token'''

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
  data = request.data
  try:
    # we will input name,email and password and in DB it will be assigned as first_name,username and password.
    # WE can further log in using the email as username
    user = User.objects.create(
      first_name = data['name'],
      # here we are updating the username with email value. So in future we can log in using this username or email
      # BUT, how we'll update the username if the email is changed?
      # We need to use Django Signals(defined in base/signals.py)
      username = data['email'],
      email = data['email'],
      password = make_password(data['password'])
    )
    serializer = UserSerializerWithToken(user,many=False)
    return Response(serializer.data)
  except:
    # making sure the email is unique for each users
    # here message has a key called detail so in frontend we will access the value using this key
    message = {'detail':'User with same email exists'}
    return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
# we need to be logged in to chane the profile
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
  user = request.user
  # We are using this serialize bcs this will give us the token that we can use to authenticate users
  serializer = UserSerializerWithToken(user,many=False)
  data = request.data
  user.first_name = data['name']
  user.username = data['email']
  user.email = data['email']

  if data['password'] != '':
    user.password = make_password(data['password'])

  user.save()
  return Response(serializer.data)



# we are using 'GET' option so we will get the user detail only when we use get method
# what's use of this api_view thing?
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
  # here user we are getting from the token api that will return the user
  # instead of the django user. Since we are using token authentication
  user = request.user
  serializer = UserSerializer(user,many=False)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
  users = User.objects.all()
  serializer = UserSerializer(users,many=True)
  return Response(serializer.data)



@api_view(['PUT'])
# Admin will be updating the users
@permission_classes([IsAuthenticated])
def updateUser(request,pk):
  user = User.objects.get(id=pk)
  data = request.data

  user.first_name = data['name']
  user.username = data['email']
  user.email = data['email']

# admin can also make any user admin
  user.is_staff = data['isAdmin']

  user.save()
  serializer = UserSerializer(user,many=False)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request,pk):
  user = User.objects.get(id=pk)
  serializer = UserSerializer(user,many=False)
  return Response(serializer.data)




@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUsers(request,pk):
  user = User.objects.get(id=pk)
  user.delete()
  return Response('User Deleted!')


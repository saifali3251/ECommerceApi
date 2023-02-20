from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product,Order,OrderItem,ShippingAddress,Review
# Why we need this token??
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
  name = serializers.SerializerMethodField(read_only=True)
  _id = serializers.SerializerMethodField(read_only=True)
  isAdmin = serializers.SerializerMethodField(read_only=True)

  class Meta:
    model = User
    # Adding only those fields which we want
    fields = ['id','_id','username','email','name','isAdmin']

  # This method will create custom attr. called name which will store first_name from django. 
  # Also if name is not provided, it will store email passed. 
  # So thi is how we add custom fields without updating the DB.This is easy approach
  def get_name(self,obj):
    name = obj.first_name
    if name == '':
      name = obj.email
    return name

  # Since in our model we used _id but django return id. So here we are updating the _id value by id
  # we created the _id field and then updating this using the id we are receiving
  def get__id(self,obj):
    _id = obj.id
    return _id

  # Creating one more custom field called isAdmin which stores the is_staff value
  def get_isAdmin(self,obj):
    isAdmin = obj.is_staff
    return isAdmin


# why we need this class?
# This class is same as above class except it will return token also.
# We need this class when a new user registers or the user credentials are changed etc so 
# They can send the token and it can be updated accordingly
class UserSerializerWithToken(UserSerializer):
  token = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = User
    fields = ['id','_id','username','email','name','isAdmin','token']

  def get_token(self,obj):
    token = RefreshToken.for_user(obj)
    # this makes the token type as assess_token since we use access_token for validating.
    # There are two types of tokens, refresh token and access token. For authentication we need access_token instead of refresh token
    return str(token.access_token)




# We want to add review with Produt Details Screen
class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = '__all__'




class ProductSerializer(serializers.ModelSerializer):
  # This is how we do nesting of a serializer into another srrializer
  reviews = serializers.SerializerMethodField(read_only=False)
  class Meta:
    model = Product
    fields = '__all__'

  def get_reviews(self,obj):
    reviews = obj.review_set.all()
    serializer = ReviewSerializer(reviews,many=True)
    return serializer.data


class OrderItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderItem
    fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = ShippingAddress
    fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
  orderItems = serializers.SerializerMethodField(read_only=True)
  shippingAddress = serializers.SerializerMethodField(read_only=True)
  user = serializers.SerializerMethodField(read_only=True)

  class Meta:
    model = Order
    fields = '__all__'

  def get_orderItems(self,obj):
    items = obj.orderitem_set.all()
    serrializer = OrderItemSerializer(items,many=True)
    return serrializer.data

  def get_shippingAddress(self,obj):
    try :
      address = ShippingAddressSerializer(obj.shippingaddress,many=False).data
    except:
      address = False
    return address

  def get_user(self,obj):
    user = obj.user
    serializer = UserSerializer(user,many=False)
    return serializer.data

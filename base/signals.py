# We are using pre_save(firing off this updateUser before saving using this pre_save)
from django.db.models.signals import pre_save
from django.contrib.auth.models import User


def updateUser(sender,instance,**kwargs):
  # print("Signal Triggered!")
  user = instance
  if user.email != '':
    user.username = user.email


# So this will get triggered once the User is created
pre_save.connect(updateUser,sender=User)

# After this, we need to connect this singnal to our respective apps
# SO we add ready method in apps.py
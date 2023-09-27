from django.contrib import admin
from.models import Product
from.models import Category
from.models import Topic
from.models import FriendList
from.models import Profile
from.models import XboxTopic

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(FriendList)
admin.site.register(Profile)
admin.site.register(XboxTopic)

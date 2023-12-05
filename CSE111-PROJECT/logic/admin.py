from django.contrib import admin
from .models import Poll, Topic, Message, Profile, Vote

# registering the models here.
admin.site.register(Poll)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(Vote)

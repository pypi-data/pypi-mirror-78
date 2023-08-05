from django.contrib import admin

from polls.models import *
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Post_test)
# Register your models here.

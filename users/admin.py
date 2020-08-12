from django.contrib import admin

from users.models import *

class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-dt']

admin.site.register(Data, ArticleAdmin)
admin.site.register(Email)
admin.site.register(Machine)
admin.site.register(MailStatus)
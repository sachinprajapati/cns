from django.contrib import admin

from users.models import Data

class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-dt']

admin.site.register(Data, ArticleAdmin)
from django.contrib import admin

# Register your models here.
# ここから下を追加
from blog.models import Category, Blog

# ここから下を追加


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'postdate', 'category')
# ここまでを追加


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)

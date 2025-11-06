from django.contrib import admin

# Register your models here.
# ここから下を追加
from blog.models import Category, Blog

# ここから下を追加


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'postdate', 'category')
# ここまでを追加


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


admin.site.register(Category, CategoryAdmin)  # 修正
admin.site.register(Blog, BlogAdmin)

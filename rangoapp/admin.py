from django.contrib import admin
from rangoapp.models import Category, Page, UserProfile

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'slug']}),
        ('Views & Likes', {'fields': ['likes', 'views']}),
    ]
    search_fields = ['name']
    prepopulated_fields = {'slug': ("name", )}


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'url', 'category']}),
        ('Views & Likes', {'fields': ['views']}),
    ]
    search_fields = ['title']
    list_display = ('title', 'category', 'url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
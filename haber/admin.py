from django.contrib import admin

# Register your models here.
from haber.models import Category, Haber


class HaberAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'category']
    list_filter = ['status' , 'category']

class CategoryAdmin(admin.ModelAdmin):
        list_display = ['title', 'status']
        list_filter = ['status']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Haber, HaberAdmin)

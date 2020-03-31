from django.contrib import admin

# Register your models here.
from haber.models import Category, Haber, Images

class HaberImagesInline(admin.TabularInline):
    model = Images
    extra = 5


class HaberAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'category', 'image']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [HaberImagesInline]



class CategoryAdmin(admin.ModelAdmin):
        list_display = ['title', 'status']
        list_filter = ['status']


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'haber', 'image_tag']
    readonly_fields = ('image_tag',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Haber, HaberAdmin)
admin.site.register(Images, ImagesAdmin)

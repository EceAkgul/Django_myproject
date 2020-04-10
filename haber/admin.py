from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

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

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_habers_count', 'related_habers_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Haber,
                'category',
                'habers_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Haber,
                 'category',
                 'habers_count',
                 cumulative=False)
        return qs

    def related_habers_count(self, instance):
        return instance.products_count
    related_habers_count.short_description = 'Related habers (for this specific category)'

    def related_habers_cumulative_count(self, instance):
        return instance.habers_cumulative_count
    related_habers_cumulative_count.short_description = 'Related habers (in tree)'




admin.site.register(Category, CategoryAdmin2)
admin.site.register(Haber, HaberAdmin)
admin.site.register(Images, ImagesAdmin)

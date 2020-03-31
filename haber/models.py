from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class Category(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=30)
    description =models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    image = models.ImageField(blank=True , upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)

    slug = models.SlugField()
    parent = models.ForeignKey('self' , blank=True, null=True, related_name='children' , on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def image_tag(self):
        return mark_safe('<img src ="{}" height="50" />'.format(self.image.url))

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title


class Haber(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description =models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    detail = models.TextField()
    status=models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def image_tag(self):
        return mark_safe('<img src ="{}" height="50" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'




class Images(models.Model):
    haber = models.ForeignKey(Haber, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'







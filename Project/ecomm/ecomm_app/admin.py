from django.contrib import admin
from ecomm_app.models import product


class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','cat','is_active']
    list_filter=['cat','is_active']


admin.site.register(product,ProductAdmin)

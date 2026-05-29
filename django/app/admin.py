from django.contrib import admin
import app.models as models

class PurchaseAdmin(admin.ModelAdmin):
    # add readonly fields, calculated_total and products
    readonly_fields = ('calculated_total', 'products')

# Register your models here.
admin.site.register(models.Supermarket)
admin.site.register(models.Employee)
admin.site.register(models.Warehouse)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.Order)
admin.site.register(models.Product)
admin.site.register(models.Distributor)
admin.site.register(models.Section)
admin.site.register(models.Client)
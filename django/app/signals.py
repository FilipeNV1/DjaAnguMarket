from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem, WareHStock, Warehouse

@receiver(post_save, sender=OrderItem)
def update_stock_on_order_item_created(sender, instance, created, **kwargs):
    """
    Update stock in all warehouses when a new OrderItem is created
    """
    if created:
        order = instance.order
        supermarket = order.supermarket
        product = instance.product
        quantity = instance.quantity
        
        # all warehouses of the supermarket
        warehouses = Warehouse.objects.filter(supermarket=supermarket)
        
        for warehouse in warehouses:
            stock, _ = WareHStock.objects.get_or_create(
                warehouse=warehouse,
                product=product,
                defaults={'wqty': 0}
            )
            stock.wqty += quantity
            stock.save()

@receiver(post_delete, sender=OrderItem)
def decrease_stock_on_order_item_deleted(sender, instance, **kwargs):
    """
    Decrease stock in all warehouses when an OrderItem is deleted
    """
    order = instance.order
    supermarket = order.supermarket
    product = instance.product
    quantity = instance.quantity
    
    # all warehouses of the supermarket
    warehouses = Warehouse.objects.filter(supermarket=supermarket)
    for warehouse in warehouses:
        try:
            stock = WareHStock.objects.get(warehouse=warehouse, product=product)
            stock.wqty = max(0, stock.wqty - quantity)
            stock.save()
        except WareHStock.DoesNotExist:
            pass

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from inventory.models import Product, ProductUnitImage

from .bag import Bag


def bag_summary(request):
    bag = Bag(request)
    product_unit_images = ProductUnitImage.objects.filter(
        is_product_unit_default=True, is_active=True)[:6]

    return render(request, 'bag/summary.html', {'bag': bag, 'product_unit_images': product_unit_images})


def bag_add(request):
    bag = Bag(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        bag.add(product=product, qty=product_qty)

        bagqty = bag.__len__()
        response = JsonResponse({'qty': bagqty})
        return response


def bag_update(request):
    bag = Bag(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        bag.update(product=product_id, qty=product_qty)

        bagqty = bag.__len__()
        bagsubtotal = bag.get_subtotal_price()
        response = JsonResponse({'qty': bagqty, 'subtotal': bagsubtotal})
        return response


def bag_delete(request):
    bag = Bag(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        bag.delete(product=product_id)

        bagqty = bag.__len__()
        bagtotal = bag.get_total_price()
        response = JsonResponse({'qty': bagqty, 'subtotal': bagtotal})
        return response

from decimal import Decimal

from django.conf import settings
from inventory.models import Product
from checkout.models import DeliveryOptions


class Bag:
    def __init__(self, request):
        self.session = request.session
        bag = self.session.get(settings.BAG_SESSION_ID)
        if settings.BAG_SESSION_ID not in request.session:
            bag = self.session[settings.BAG_SESSION_ID] = {}
        self.bag = bag

    def add(self, product, qty):
        product_id = str(product.id)

        if product_id in self.bag:
            self.bag[product_id]["qty"] = qty
        else:
            self.bag[product_id] = {"price": str(
                product.retail_price), "qty": qty}

        self.save()

    def __iter__(self):
        product_ids = self.bag.keys()
        products = Product.objects.filter(id__in=product_ids)
        bag = self.bag.copy()

        for product in products:
            bag[str(product.id)]["product"] = product

        for item in bag.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        return sum(item["qty"] for item in self.bag.values())

    def update(self, product, qty):
        product_id = str(product)
        if product_id in self.bag:
            self.bag[product_id]["qty"] = qty
        self.save()

    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.bag.values())

    def get_delivery_price(self):
        newprice = 0.00

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(
                id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice

    def get_total_price(self):
        newprice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"]
                       for item in self.bag.values())

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(
                id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    def bag_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"]
                       for item in self.bag.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    def delete(self, product):
        product_id = str(product)

        if product_id in self.bag:
            del self.bag[product_id]
            self.save()

    def clear(self):
        del self.session[settings.BAG_SESSION_ID]
        # del self.session["address"]
        # del self.session["purchase"]
        self.save()

    def save(self):
        self.session.modified = True

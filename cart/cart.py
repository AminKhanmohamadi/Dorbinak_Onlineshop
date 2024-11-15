from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from products.models import Product


class Cart:
    def __init__(self , request):
        """

            Initialize a new 'Cart' object.

        """


        self.request = request
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart






    def add(self , product ,quantity=1 , replace_current_quantity=False ):
        """

            Add a product to the cart.

        """

        product_id = str(product.id)


        if product_id not in self.cart:
            self.cart[product_id] = {'quantity' : 0}


        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        messages.success(self.request, _('Successfully added to cart'))

        self.save()







    def save(self):
        """
            save the cart to the session.
        """
        self.session.modified = True




    def remove(self , product):
        """

            Remove a product from the cart.

        """

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.error(self.request, _('Successfully removed from cart'))
            self.save()





    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)


        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].get_price() * item['quantity']


            yield item




    def __len__(self):
        return len(self.cart.values())




    def clear(self):
        del self.session['cart']
        self.save()



    def get_total_price(self):
        product_ids = self.cart.keys()

        return sum(item['quantity'] * item['product_obj'].get_price() for item in self.cart.values())
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.urls import urlpatterns

from django.contrib.auth.models import User
from .models import Store, Category, OrderProduct, Profile

from .utils.logs import logged_function
import logging

from django.http import HttpResponse

@logged_function
def index(request):

    stores = Store.objects.all()

    context = {'stores': stores }
    
    return render(request, 'ordering/index.html', context)


@logged_function
@login_required
def store(request, store_identifier, store_category_id=''):
    store_result = get_object_or_404(
        Store, url_identifying_name=store_identifier)

    category = Category.find_category_given_category_pk_and_store_pk(
        category_pk=store_category_id, store_pk=store_result.id)

    category_products = category.get_products()

    displayed_items = [
            category_product.convert_to_box_selection() for category_product in category_products]
    
    print(displayed_items)
            

    products_in_cart = OrderProduct.get_products_in_cart_for_user(
        user_pk=request.user.pk)

    context = {'store': store_result, 'category': category,
               'displayed_items': displayed_items, 'products_in_cart': products_in_cart }
    return render(request, 'ordering/store.html', context)


@logged_function
@login_required
def add_to_cart(request, store_id, store_category_id):
    logging.debug(request.POST)

    store_result = get_object_or_404(
        Store, id=store_id)

    try:
        product_to_add_id = request.POST['product_to_add']
        User.objects.get(pk=request.user.pk).profile.add_product_to_cart(
            product_to_add_id)
    except Exception as e:
        logging.error(e.__str__())

    return HttpResponseRedirect(reverse('ordering:store', args=(store_result.url_identifying_name, store_category_id)))

import logging

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.urls import urlpatterns

from .models import Store, Category, OrderProduct, User

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


def index(request, store_identifier, store_category_id=''):
    logging.debug('index called')

    store_result = get_object_or_404(
        Store, url_identifying_name=store_identifier)

    category = Category.find_category_given_category_pk_and_store_pk(
        category_pk=store_category_id, store_pk=store_result.id)

    products_in_cart = OrderProduct.get_products_in_cart_for_user(
        user_pk=1)

    context = {'store': store_result, 'category': category,
               'products_in_cart': products_in_cart}
    return render(request, 'ordering/index.html', context)


@login_required
def add_to_cart(request, store_id, store_category_id):
    logging.debug('add_to_cart called')
    logging.debug(request.POST)

    store_result = get_object_or_404(
        Store, id=store_id)

    try:
        product_to_add_id = request.POST['product_to_add']
        User.objects.get(pk=1).add_product_to_cart(product_to_add_id)
    except Exception as e:
        pass

    return HttpResponseRedirect(reverse('ordering:index', args=(store_result.url_identifying_name, store_category_id)))

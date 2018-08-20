import logging

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Store, Category, OrderProduct

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


def index(request, store_identifier, store_category_id=''):
    logging.debug('index called')

    store_result = get_object_or_404(
        Store, url_identifying_name=store_identifier)

    category = Category.find_category_given_category_pk_and_store_pk(
        category_pk=store_category_id, store_pk=store_result.id)

    products_in_cart = OrderProduct.get_products_in_cart_for_user(user_pk=1)

    context = {'store': store_result, 'category': category, 'products_in_cart': products_in_cart}
    return render(request, 'ordering/index.html', context)


def add_to_cart(request, store_identifier, store_category_id):
    logging.debug('add_to_cart called')
    logging.debug(request.POST)
    return HttpResponseRedirect(reverse('ordering:index', args=(store_identifier, store_category_id)))

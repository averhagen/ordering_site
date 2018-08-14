import logging

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Store, StoreCategory, Order

logging.basicConfig(filename='views.log', level=logging.DEBUG)


def index(request, store_identifier, store_category_id=''):
    logging.debug('index called')

    store_result = get_object_or_404(
        Store, url_identifying_name=store_identifier)

    category = StoreCategory.find_category_given_category_pk_and_store_pk(
        category_pk=store_category_id, store_pk=store_result.id)

    orders = Order.find_orders_for_store_and_user(
        user_id=1, store_id=store_result.id)

    context = {'store': store_result, 'category': category, 'orders': orders}
    return render(request, 'ordering/index.html', context)


def add_to_cart(request, store_identifier, store_category_id):
    logging.debug('add_to_cart called')
    logging.debug(request.POST)
    return HttpResponseRedirect(reverse('ordering:index', args=(store_identifier, store_category_id)))

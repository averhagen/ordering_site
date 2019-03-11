from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.urls import urlpatterns
from django.contrib.auth.models import User

from .models import Store, StoreStyle, Category, OrderProduct, Profile
from .components import MenuSelection
from .utils.logs import logged_function

import logging

from django.http import HttpResponse

@logged_function
def index(request):

    stores = Store.objects.all()

    context = {'stores': stores }
    
    return render(request, 'ordering/index.html', context)


@logged_function
def store_style(request, style_id):
    style = get_object_or_404(StoreStyle, id=style_id)
    context = {'primary_color': style.primary_color, 'secondary_color': style.secondary_color}
    context['tertiary_color'] = style.tertiary_color
    context['font_color'] = "#000000"
    response = render(request, 'theme.css', context)
    response['Content-Type'] = 'text/css'
    return response


@logged_function
@login_required
def store(request, store_identifier, store_category_id=''):
    store_result = get_object_or_404(
        Store, url_identifying_name=store_identifier)

    products_in_cart = OrderProduct.get_products_in_cart_for_user(
        user_pk=request.user.pk)

    selected_category = Category.find_category_given_category_pk_and_store_pk(
        category_pk=store_category_id, store_pk=store_result.id)
    
    menu_selections = []

    for category in store_result.get_categories_sorted_by_display_order():
        url = reverse('ordering:store', args=[store_result.url_identifying_name,category.id])
        category_is_selected = selected_category is not None and category.id == selected_category.id
        menu_selection = MenuSelection(category.display_name, url, category_is_selected)
        menu_selections.append(menu_selection)

    if selected_category is not None:
        displayed_items = [
                category_product.convert_to_box_selection() for category_product in selected_category.get_products()]
    else:
        displayed_items = []
        
    context = {'store': store_result, 'category': selected_category, 'menu_selections': menu_selections,
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

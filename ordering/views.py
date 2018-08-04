from django.shortcuts import get_object_or_404, render

from .models import Store, StoreCategory, Order


def index(request, store_identifier, store_category_id=''):
    store_result = get_object_or_404(
        Store, url_identifying_name=store_identifier)
    category = None
    if isinstance(store_category_id, int):
        try:
            category = StoreCategory.objects.get(pk=store_category_id)
            if category.store != store_result:
                category = None
        except StoreCategory.DoesNotExist:
            pass
    orders = Order.find_orders_for_store_and_user(user_id=1, store_id=store_result.id)
    context = {'store': store_result, 'category': category, 'orders': orders}
    return render(request, 'ordering/index.html', context)

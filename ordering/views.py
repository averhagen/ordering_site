from django.shortcuts import get_object_or_404, render

from .models import Store, StoreCategory

# Create your views here.


def index(request, store_identifier, store_category_id=''):
    store = get_object_or_404(Store, url_identifying_name=store_identifier)
    category = None
    if isinstance(store_category_id, int):
        try:
            category = StoreCategory.objects.get(pk=store_category_id)
            if category.store != store:
                category = None
        except StoreCategory.DoesNotExist:
            pass
    context = {'store': store, 'category': category}
    return render(request, 'ordering/index.html', context)

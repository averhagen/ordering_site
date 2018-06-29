from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Store, StoreCategory

# Create your views here.


def index(request, store_identifier, store_category_id=''):
    store = get_object_or_404(Store, url_identifying_name=store_identifier)
    category = None
    try:
        category = StoreCategory.objects.get(pk=store_category_id)
    except StoreCategory.DoesNotExist:
        pass
    context = {'store': store, 'category': category}
    return render(request, 'ordering/index.html', context)

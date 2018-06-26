from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Store

# Create your views here.
def index(request, store_identifier):
    store = get_object_or_404(Store, url_identifying_name = store_identifier)
    context = {'store': store, 'menuchoices': ['a', 'b', 'c']}
    return render(request, 'ordering/index.html', context)
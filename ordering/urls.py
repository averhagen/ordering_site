from django.urls import path
from . import views


app_name = 'ordering'

urlpatterns = [
    path('<int:store_id>/<int:store_category_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<store_identifier>/', views.index, name='index'),
    path('<store_identifier>/<int:store_category_id>', views.index, name='index'),
]

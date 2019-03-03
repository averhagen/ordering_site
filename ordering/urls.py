from django.urls import path
from . import views


app_name = 'ordering'

urlpatterns = [
    path('', views.index, name='index'),
    path('theme/<int:store_id>', views.store_style, name='store_style'),
    path('<int:store_id>/<int:store_category_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<store_identifier>/', views.store, name='store'),
    path('<store_identifier>/<int:store_category_id>', views.store, name='store'),
]

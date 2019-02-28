from django.urls import path
from . import views


app_name = 'ordering'

urlpatterns = [
    path('', views.index, name='index'),
    path('theme/<store_identifier>', views.theme, name='theme'),
    path('<int:store_id>/<int:store_category_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<store_identifier>/', views.store, name='store'),
    path('<store_identifier>/<int:store_category_id>', views.store, name='store'),
]

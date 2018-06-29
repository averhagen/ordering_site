from django.urls import path
from . import views


app_name = 'ordering'

urlpatterns = [
    path('<store_identifier>/', views.index, name = 'index' ),
    path('<store_identifier>/<int:store_category_id>', views.index, name = 'index')
]
from django.urls import path

from . import views

urlpatterns = [
    path('<store_identifier>', views.index, name = 'index' )
]
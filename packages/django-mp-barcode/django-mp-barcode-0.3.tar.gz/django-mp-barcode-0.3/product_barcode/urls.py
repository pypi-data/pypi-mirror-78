
from django.urls import path

from product_barcode import views


app_name = 'barcode'


urlpatterns = [

    path('print/', views.print_codes, name='print'),

    path('img/<str:code>/', views.get_code, name='get')

]

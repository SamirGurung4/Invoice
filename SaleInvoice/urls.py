from django.urls import path
from .views import InvoiceListView, create_invoice

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),
    path('create_invoice/', create_invoice, name='create_invoice'),
]


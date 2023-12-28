# views.py

from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django import forms
from .models import Invoice, InvoiceItem, Customer, Product


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        queryset = super().get_queryset()
        invoice_id = self.request.GET.get('invoice_id')

        if invoice_id:
            queryset = queryset.filter(Invoice_ID=invoice_id)

        return queryset


def create_invoice(request):
    InvoiceForm = forms.modelform_factory(Invoice, fields=['Date', 'Payment_method', 'Customer', 'Tax'])
    InvoiceItemForm = forms.modelform_factory(InvoiceItem, fields=['Product', 'Quantity'])

    context = {
        "invoice_form": InvoiceForm,
        "invoice_item": InvoiceItemForm,
        "products": Product.objects.all(),
    }

    if request.method == 'POST':
        date = request.POST.get('Date')
        payment_method = request.POST.get('Payment_method')
        customer_name = request.POST.get('Customer')
        tax = request.POST.get('Tax')
        Total_Amount = request.POST.get('Total')

        tax_rate = Decimal('0.13')

        print(request.POST)
        customer, created = Customer.objects.get_or_create(Name=customer_name)

        # Fetching tax and product details
        tax = Decimal(request.POST.get('Tax', 0))
        product_name = request.POST.get("Product")
        quantity = request.POST.get('Quantity')

        try:
            selected_product = Product.objects.get(Product_Name=product_name)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'errors': {'Product': 'Selected product does not exist.'}})

        # Calculate total amount, tax, and save to the database
        total_amount = (selected_product.Price * Decimal(quantity)) + tax

        invoice_data = InvoiceForm({
            'Date': date,
            'Payment_method': payment_method,
            'Customer': customer.Customer_ID,
            'Tax': tax,
            'Total_Amount': total_amount,
        })

        if invoice_data.is_valid():
            invoice = invoice_data.save()

            # Create InvoiceItem with details from Product
            invoice_item = InvoiceItem.objects.create(
                Invoice=invoice,
                Product=selected_product,
                Quantity=quantity,
                Price=selected_product.Price
            )

            # If using ManyToManyField, add the product to the invoice's Products
            invoice.Products.add(selected_product)

            # Set Tax and Total_Amount fields of the Invoice model
            invoice.Tax = tax

            # Update Total_Amount to include both product price * quantity and tax
            invoice.Total_Amount = (selected_product.Price * Decimal(quantity)) + tax

            # Save changes to the Invoice model
            invoice.save()

            messages.success(request, 'Invoice created successfully!')
            return redirect('invoice_list')
        return JsonResponse({'success': False, 'errors': invoice_data.errors})

    return render(request, "invoice.html", context)

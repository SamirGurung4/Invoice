from django.db import models


class Customer(models.Model):
    Customer_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name


class Product(models.Model):
    Product_ID = models.AutoField(primary_key=True)
    Product_Name = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.Product_Name


class Invoice(models.Model):
    Invoice_ID = models.AutoField(primary_key=True)
    Date = models.DateField()
    Payment_method = models.CharField(max_length=50)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Products = models.ManyToManyField(Product, through='InvoiceItem')
    Tax = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    Total_Amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0)

    def __str__(self):
        return f"Invoice {self.Invoice_ID}"

    def calculate_total_amount(self):
        total_amount = sum(item.Product.Price * item.Quantity for item in self.invoiceitem_set.all())
        return total_amount


class InvoiceItem(models.Model):
    Invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.PositiveIntegerField(default=0)
    Price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.Price = self.Product.Price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.Invoice.Invoice_ID} - {self.Product.Product_Name}"

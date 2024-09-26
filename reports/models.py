# Create your models here.
from django.db import models
from orders.models import Order  # Asegúrate de que este sea el nombre correcto del modelo Order

class SalesReport(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    report_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)  # Podría ser "completed", "pending", etc.

    def __str__(self):
        return f"Report for Order ID: {self.order.id} on {self.report_date}"
